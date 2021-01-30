/* eslint-disable max-classes-per-file */
import { Sprite, Texture } from 'pixi.js';
import { si, Spline, createSpline, evalSpline, Vec2 } from '.';

type InterpolationData = {
  position: Vec2;
  velocity: Vec2;
};

function parseData(data: Partial<si.EntityData>): InterpolationData {
  return {
    position: data.position ? (data.position as Vec2) : [0, 0],
    velocity: data.velocity ? (data.velocity as Vec2) : [0, 0],
  };
}

export class InterpolatedSprite extends Sprite {
  public interpolationSpline: Spline;
  public _destroyed = false;
  private interpolationData: InterpolationData;

  constructor(texture: Texture, data: Partial<si.EntityData>) {
    super(texture);
    this.interpolationData = parseData(data);
    this.position.set(this.interpolationData.position[0], this.interpolationData.position[1]);

    // initial splines
    this.interpolationSpline = {
      a: this.interpolationData.position,
      b: [0, 0],
      c: [0, 0],
      d: this.interpolationData.position,
    };
  }

  public interpolate(): void {
    const [x, y] = evalSpline(this.interpolationSpline, 0);
    this.position.set(x, y);
  }

  public recalculateInterpolation(
    data: Partial<si.EntityData>,
    serverDeltaTime: number,
    localDeltaFrames: number,
    velocityCorrection?: number,
  ): void {
    const vc = velocityCorrection ?? 0.5 * serverDeltaTime;

    const oldData = this.interpolationData;
    const oldPos: Vec2 = [this.position.x, this.position.y];
    const newData = parseData(data);

    this.interpolationSpline = createSpline(
      oldPos,
      oldData.velocity,
      newData.position,
      newData.velocity,
      serverDeltaTime,
      vc,
    );

    this.interpolationData = newData;
  }
}
