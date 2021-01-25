import { Application } from 'pixi.js';
import { ci, Client } from './lib';
import { Keyboard, Key, KeyboardContext } from './lib/keyboard';

export class App {
  private client: Client;
  private keyboard: Keyboard;

  constructor(app: Application, client: Client, keyboard: Keyboard) {
    this.client = client;
    this.keyboard = keyboard;
  }

  public async init(): Promise<void> {
    await this.initClient();
    this.initKeyboard();
  }

  private async initClient(reconnect = false): Promise<void> {
    const timeout = reconnect ? 15000 : 10000;
    await this.client.connect(timeout);
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
