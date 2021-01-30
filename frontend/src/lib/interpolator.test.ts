import { RenderTexture } from 'pixi.js';
import { evalSpline } from './spline';
import { InterpolatedSprite } from './interpolation';

const mockTexture = RenderTexture.create();

describe('InterpolatedSprite', () => {
  it('initializes Spline from current position to current position', () => {
    const initialPosition = [1, 2];
    const sprite = new InterpolatedSprite(mockTexture, {
      position: initialPosition,
      velocity: [0, 0],
    });
    expect(sprite.interpolationSpline).toEqual({ a: initialPosition, b: [0, 0], c: [0, 0], d: initialPosition });
  });

  describe('recalculateInterpolation', () => {
    const initialPosition = [1, 2];
    let sprite: InterpolatedSprite;
    beforeEach(() => {
      sprite = new InterpolatedSprite(mockTexture, {
        position: initialPosition,
        velocity: [0, 0],
      });
    });

    it('initial point evaluates to current location', () => {
      sprite.recalculateInterpolation(
        {
          position: [5, 5],
          velocity: [0, 0],
        },
        1,
        1,
        1,
      );
      expect([sprite.position.x, sprite.position.y]).toEqual([1, 2]);
      expect(evalSpline(sprite.interpolationSpline, 0)).toEqual([1, 2]);
    });

    it('end point evaluates to target location with velocity=0', () => {
      sprite.recalculateInterpolation(
        {
          position: [5, 5],
          velocity: [0, 0],
        },
        1,
        1,
        1,
      );
      expect(evalSpline(sprite.interpolationSpline, 1)).toEqual([5, 5]);
    });

    it('end point evaluates to target location + velocity * t', () => {
      sprite.recalculateInterpolation(
        {
          position: [5, 5],
          velocity: [2, 3],
        },
        2,
        1,
        1,
      );
      expect(evalSpline(sprite.interpolationSpline, 1)).toEqual([5 + 2 * 2, 5 + 3 * 2]);
    });

    it('excess frames do extrapolate spline', () => {
      sprite.recalculateInterpolation(
        {
          position: [5, 5],
          velocity: [1, 1],
        },
        1,
        10,
        1,
      );
      sprite.interpolate(10);
      expect([sprite.position.x, sprite.position.y]).toEqual([6, 6]);
      sprite.interpolate(20);
      expect([sprite.position.x, sprite.position.y]).toEqual([8, 8]);
    });
  });
});
