import { Application, IResourceDictionary } from 'pixi.js';
import { ci, Client, loadResources } from './lib';
import { Keyboard, Key, KeyboardContext } from './lib/keyboard';
import { Game } from './game';
import { RESOURCES } from './constants';

export class App {
  private client: Client;
  private keyboard: Keyboard;
  private game: Game;
  private resources: IResourceDictionary = {};

  constructor(app: Application, client: Client, keyboard: Keyboard, game: Game) {
    this.client = client;
    this.keyboard = keyboard;
    this.game = game;
  }

  public async init(): Promise<void> {
    await this.initClient();
    this.initKeyboard();
  }

  private async initClient(reconnect = false): Promise<void> {
    const timeout = reconnect ? 15000 : 10000;
    await this.initResources();
    await this.client.connect(timeout);
  }

  private async initResources(): Promise<void> {
    try {
      this.resources = await loadResources(RESOURCES);
      this.game.initResources(this.resources);
    } catch (err) {
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
