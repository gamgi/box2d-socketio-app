import { Application } from 'pixi.js';
import { Client, Keyboard } from './lib';
import { getClientConfig } from './apiConfig';
import { App } from './app';
import { Game } from './game';

async function init(pixi: Application) {
  const clientConfig = getClientConfig();
  const client = new Client(clientConfig);
  const keyboard = new Keyboard();
  const game = new Game(pixi, client);
  const app = new App(pixi, client, keyboard, game);
  await app.init(true);

  while (true) {
    await app.run();
    // eslint-disable-next-line no-console
    console.log('reconnecting');
    await app.reconnect();
  }
}

void init(
  new Application({
    width: 800,
    height: 600,
    view: getCanvas(),
    antialias: true,
    transparent: false,
    resolution: 1,
  }),
);

function getCanvas(): HTMLCanvasElement {
  const canvas = document.querySelector<HTMLCanvasElement>('#canvas');
  if (!canvas) {
    throw new Error('could not find canvas');
  }
  return canvas;
}
