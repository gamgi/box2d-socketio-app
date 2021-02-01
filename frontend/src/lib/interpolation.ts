/* eslint-disable max-classes-per-file */
import { Application, Sprite } from 'pixi.js';
import { RingBuffer, Spline, createLinear, createSpline, evalSpline, Vec2 } from '.';

export type InterpolationData = {
  position: Vec2;
  velocity: Vec2;
};

const isDestroyed = (sprite: Sprite): boolean => {
  // eslint-disable-next-line no-underscore-dangle
  return ((sprite as unknown) as Record<'_destroyed', boolean>)._destroyed === true;
};

export class InterpolatedSprite {
  public interpolationSpline: Spline;
  public extrapolationLine: Spline;
  private interpolationFrame = 0;
  private interpolationFrames = 1;
  private interpolationData: InterpolationData;

  constructor(public sprite: Sprite, data: InterpolationData) {
    this.interpolationData = data;
    this.sprite.position.set(this.interpolationData.position[0], this.interpolationData.position[1]);

    // initial splines
    this.interpolationSpline = {
      a: this.interpolationData.position,
      b: [0, 0],
      c: [0, 0],
      d: this.interpolationData.position,
    };
    this.extrapolationLine = createLinear(this.interpolationData.position, [0, 0], 0);
  }

  public interpolate(frames: number): void {
    this.interpolationFrame += frames;
    const t = this.interpolationFrame / this.interpolationFrames;

    const [x, y] =
      t <= 1
        ? evalSpline(this.interpolationSpline, t) // interpolate
        : evalSpline(this.extrapolationLine, t - 1); // extrapolate
    this.sprite.position.set(x, y);
  }

  public recalculateInterpolation(newData: InterpolationData, serverDeltaTime: number, localDeltaFrames: number): void {
    const oldData = this.interpolationData;
    const oldPos: Vec2 = [this.sprite.position.x, this.sprite.position.y];
    const oldVelocity: Vec2 = oldData.velocity;
    const newVelocity: Vec2 = newData.velocity;
    // TODO check spline equations, since this correction constant is odd
    const vc = serverDeltaTime / 2;

    this.interpolationSpline = createSpline(oldPos, oldVelocity, newData.position, newVelocity, serverDeltaTime, vc);
    this.extrapolationLine = createLinear(newData.position, newVelocity, serverDeltaTime, vc);

    this.interpolationData = newData;
    this.interpolationFrame = 0;
    this.interpolationFrames = localDeltaFrames;
  }
}

export class Interpolator {
  private packetFrameDelayBuffer: RingBuffer = new RingBuffer(5, 1);
  private packetDelayBuffer: RingBuffer = new RingBuffer(5, 1);
  private tLastUpdate;
  public packetFrameDelay = 1;
  public packetDelay = 0;
  private elapsedFrames = 0;
  private sprites: InterpolatedSprite[] = [];

  constructor(pixi: Application) {
    this.tLastUpdate = performance.now();
    pixi.ticker.add(() => {
      this.elapsedFrames++;
      this.sprites = this.sprites.filter((sprite) => !isDestroyed(sprite.sprite));
      this.sprites.forEach((sprite) => sprite.interpolate(1));
    });
  }

  public getInterpolationData(): { serverDeltaTime: number; localDeltaFrames: number } {
    return { serverDeltaTime: this.packetDelay, localDeltaFrames: this.packetFrameDelay };
  }

  public onReceiveData(): void {
    this.packetFrameDelayBuffer.push(this.elapsedFrames);
    this.packetFrameDelay = Math.ceil(this.packetFrameDelayBuffer.mean());
    this.elapsedFrames = 0;

    this.packetDelayBuffer.push(performance.now() - this.tLastUpdate);
    this.packetDelay = this.packetDelayBuffer.mean() / 1000;
    this.tLastUpdate = performance.now();
  }

  public new(sprite: Sprite, data: InterpolationData): InterpolatedSprite {
    const interpolated = new InterpolatedSprite(sprite, data);
    this.sprites.push(interpolated);
    return interpolated;
  }
}
