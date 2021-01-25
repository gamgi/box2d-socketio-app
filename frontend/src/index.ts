import { Application } from 'pixi.js';
import { Client, Keyboard } from './lib';
import { HOST } from './constants';
import { App } from './app';

function init(pixi: Application) {
  const client = new Client({ url: HOST });
  const keyboard = new Keyboard();
  const app = new App(pixi, client, keyboard);

  void app.init();
}

init(
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
