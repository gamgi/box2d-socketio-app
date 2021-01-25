import { App } from './app';
import { Application } from 'pixi.js';
import { Client, Keyboard, Key } from './lib';

jest.mock('./lib/client');

describe('App', () => {
  it('init() initializes resources, keyboard and client', async () => {
    const client = new Client();
    const keyboard = new Keyboard();
    jest.spyOn(keyboard.eventEmitter, 'on');
    const game = { initResources: jest.fn() } as any;
    const app = new App(new Application(), client, keyboard, game);

    await app.init();

    expect(game.initResources).toHaveBeenCalled();
    expect(keyboard.eventEmitter.on).toHaveBeenCalled();
    expect(client.connect).toHaveBeenCalled();
  });
});
