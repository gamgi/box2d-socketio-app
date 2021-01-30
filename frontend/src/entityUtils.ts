import { Application, Sprite, Graphics, SCALE_MODES } from 'pixi.js';

export function renderGraphicToSprite(graphic: Graphics, pixi: Application): Sprite {
  const texture = pixi.renderer.generateTexture(graphic, SCALE_MODES.LINEAR, pixi.renderer.resolution);
  const sprite = new Sprite(texture);
  return sprite;
}
