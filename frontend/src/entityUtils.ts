import { Application, Sprite, Graphics, RenderTexture } from 'pixi.js';

export function renderGraphicToSprite(graphic: Graphics, pixi: Application): Sprite {
  const texture = RenderTexture.create({ width: graphic.height, height: graphic.height });
  pixi.renderer.render(graphic, texture);
  const sprite = new Sprite(texture);
  return sprite;
}
