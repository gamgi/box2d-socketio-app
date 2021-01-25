import { Application, IResourceDictionary } from 'pixi.js';
import { ci, Client, ClientError, loadResources } from './lib';
import { Keyboard, Key, KeyboardContext } from './lib/keyboard';
import { Game } from './game';
import { Ui, MessageLevel } from './ui';
import { RESOURCES } from './constants';

export class App {
  private client: Client;
  private keyboard: Keyboard;
  private game: Game;
  private ui: Ui;
  private resources: IResourceDictionary = {};

  constructor(app: Application, client: Client, keyboard: Keyboard, game: Game) {
    this.client = client;
    this.keyboard = keyboard;
    this.game = game;
    this.ui = new Ui(app);
  }

  public async init(): Promise<void> {
    await this.initResources();
    await this.initClient();
    this.initKeyboard();

    this.client.eventEmitter.on('disconnect', () => {
      this.ui.showMessage('Connection to server lost', MessageLevel.ERROR);
    });
  }

  private async initResources(): Promise<void> {
    try {
      this.ui.showMessage('Loading');
      this.resources = await loadResources(RESOURCES);
      this.game.initResources(this.resources);
    } catch (err) {
      this.ui.showMessage('Failed to load images', MessageLevel.ERROR);
      throw err;
    }
  }

  private async initClient(reconnect = false): Promise<void> {
    const timeout = reconnect ? 15000 : 10000;
    const message = reconnect ? 'Reconnecting' : 'Connecting';
    try {
      this.ui.showMessage(message);
      await this.client.connect(timeout);
      await this.game.createRoom('my room', false);
      this.ui.clearMessage();
    } catch (err) {
      if (err instanceof ClientError) {
        this.ui.showMessage(`${err.userMessage}`, MessageLevel.ERROR);
      }
      throw err;
    }
  }

  private initKeyboard(): void {
    const keyPressHander = (key: Key, context: KeyboardContext): void => {
      // eslint-disable-next-line camelcase
      const keydown: ci.InputDTO = { keys_down: context.keysDown, keys_released: null, keys_pressed: [Key[key]] };
      this.client.sendInput(keydown);
    };
    const keyReleaseHander = (key: Key, context: KeyboardContext): void => {
      // eslint-disable-next-line camelcase
      const keyup: ci.InputDTO = { keys_down: context.keysDown, keys_released: [Key[key]], keys_pressed: null };
      this.client.sendInput(keyup);
    };

    this.keyboard.eventEmitter.on('pressed', keyPressHander);
    this.keyboard.eventEmitter.on('released', keyReleaseHander);
  }

  public async run(): Promise<void> {
    return new Promise((resolve) => {
      this.client.eventEmitter.once('disconnect', () => {
        resolve();
      });
    });
  }

  public async reconnect(): Promise<void> {
    if (this.client.connected) {
      return;
    }

    return this.initClient(true);
  }
}
