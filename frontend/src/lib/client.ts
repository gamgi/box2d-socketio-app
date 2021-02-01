import { io, Socket, SocketOptions, ManagerOptions } from 'socket.io-client';
import { utils } from 'pixi.js';
import { ci, si } from './index';
import { ConnectionFailedError, ConnectionClosedError } from './clientErrors';
import { ServerError } from './serverErrors';

export type ClientOptions = {
  url: string;
} & Partial<SocketOptions & ManagerOptions>;

export class Client {
  private socket: Socket;
  public eventEmitter: utils.EventEmitter = new utils.EventEmitter();

  constructor(options: ClientOptions = { url: 'localhost:5000' }) {
    const { url, ...socketIoOptions } = options;
    this.socket = io(url, { autoConnect: false, ...socketIoOptions });

    this.socket.on('disconnect', () => {
      this.eventEmitter.emit('disconnect', null);
      this.socket.close();
    });

    this.bindSocketEventsToEmitter(['short_sync', 'long_sync']);
  }

  public async connect(timeout = 5000): Promise<void> {
    return new Promise((resolve, reject) => {
      const connectTimer = setTimeout(() => {
        this.socket.close();
        reject(new ConnectionFailedError('Connection timed out'));
      }, timeout);
      this.socket.once('connect', function () {
        clearTimeout(connectTimer);
        resolve();
      });
      this.socket.connect();
    });
  }

  public sendInput(data: ci.InputDTO): void {
    this.socket.emit('input', data);
  }

  public async createRoom(data: ci.CreateRoomDTO): Promise<si.CreateRoomDTO> {
    const response = await emitAsPromise<si.CreateRoomDTO>(this.socket, 'create_room', data);
    if (isError(response)) {
      throw new Error(response.message);
    }
    return response;
  }

  public async send<T>(eventName: string, data: Record<string, any>): Promise<T> {
    return await emitAsPromise<T>(this.socket, eventName, data);
  }

  public async sendOrFailWith<T>(eventName: string, data: Record<string, any>, userMessage: string): Promise<T> {
    try {
      return await emitAsPromise<T>(this.socket, eventName, data);
    } catch (err) {
      if (err instanceof ServerError) {
        throw new ServerError(err.message, userMessage, err.userMessage, err.code);
      }
      throw err;
    }
  }

  public get connected(): boolean {
    return this.socket.connected;
  }

  private bindSocketEventsToEmitter(events: string[]) {
    // We could refer to Client.socket directly, but this.eventEmitter has a slightly
    // differing interface (eventemitter3). So we re-emit events for consistency.
    for (const event of events) {
      this.socket.on(event, (data: any) => this.eventEmitter.emit(event, data));
    }
  }
}

function isError(response: Record<string, any> | si.ErrorDTO): response is si.ErrorDTO {
  return response.error === true;
}

function emitAsPromise<T extends Record<string, any>>(
  socket: Socket,
  event: string,
  data: Record<string, any>,
): Promise<T> {
  return new Promise((resolve, reject) => {
    const parseResponse = (response: T | si.ErrorDTO | null) => {
      if (!response) {
        reject(new ConnectionClosedError('No response from server'));
      } else if (isError(response)) {
        reject(new ServerError(response.message, 'Server error', response.message, response.code));
      } else {
        resolve(response);
      }
    };
    socket.emit(event, data, parseResponse);
  });
}
