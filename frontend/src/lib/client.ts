import { io, Socket, SocketOptions, ManagerOptions } from 'socket.io-client';
import { utils } from 'pixi.js';
import { ConnectionError } from './clientErrors';

type ClientOptions = {
  url: string;
} & Partial<SocketOptions & ManagerOptions>;

function emitAsPromise<T>(socket: Socket, event: string, data: Record<string, any>): Promise<T> {
  return new Promise((resolve, reject) => {
    const parseResponse = (response: T) => {
      if (!response) {
        reject(response as any);
      }
      resolve(response);
    };
    socket.emit(event, data, parseResponse);
  });
}

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

    this.bindSocketEventsToEmitter(['update_entities', 'fast_update_entities']);
  }

  public async connect(timeout = 5000): Promise<void> {
    return new Promise((resolve, reject) => {
      const connectTimer = setTimeout(() => {
        this.socket.close();
        reject(new ConnectionError('Connection timed out'));
      }, timeout);
      this.socket.once('connect', function () {
        clearTimeout(connectTimer);
        resolve();
      });
      this.socket.connect();
    });
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
