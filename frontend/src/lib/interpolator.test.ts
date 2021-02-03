import { Sprite, Ticker } from 'pixi.js';
import { evalSpline } from './spline';
import { Application } from 'pixi.js';
import { Interpolator, InterpolatedSprite } from './interpolation';
import { Vec2 } from './types';

const mockSprite = new Sprite();

describe('InterpolatedSprite', () => {
  it('initializes Spline from current position to current position', () => {
    const initialPosition: Vec2 = [1, 2];
    const sprite = new InterpolatedSprite(mockSprite, {
      position: initialPosition,
      velocity: [0, 0],
    });
    expect(sprite.interpolationSpline).toEqual({ a: initialPosition, b: [0, 0], c: [0, 0], d: initialPosition });
  });

  describe('recalculateInterpolation', () => {
    const initialPosition: Vec2 = [1, 2];
    let interpolated: InterpolatedSprite;
    beforeEach(() => {
      interpolated = new InterpolatedSprite(mockSprite, {
        position: initialPosition,
        velocity: [0, 0],
      });
    });

    it('initial point evaluates to current location', () => {
      interpolated.recalculateInterpolation(
        {
          position: [5, 5],
          velocity: [0, 0],
        },
        1,
        1,
      );
      expect([interpolated.sprite.position.x, interpolated.sprite.position.y]).toEqual([1, 2]);
      expect(evalSpline(interpolated.interpolationSpline, 0)).toEqual([1, 2]);
    });

    it('end point evaluates to target location with velocity=0', () => {
      interpolated.recalculateInterpolation(
        {
          position: [5, 5],
          velocity: [0, 0],
        },
        1,
        1,
      );
      expect(evalSpline(interpolated.interpolationSpline, 1)).toEqual([5, 5]);
    });

    it('end point evaluates to target location + velocity * t', () => {
      interpolated.recalculateInterpolation(
        {
          position: [5, 5],
          velocity: [2, 3],
        },
        2,
        1,
      );
      expect(evalSpline(interpolated.interpolationSpline, 1)).toEqual([5 + 2 * 2, 5 + 3 * 2]);
    });

    it('excess frames do extrapolate spline', () => {
      interpolated.recalculateInterpolation(
        {
          position: [5, 5],
          velocity: [1, 1],
        },
        1,
        10,
      );
      interpolated.interpolate(10);
      expect([interpolated.sprite.position.x, interpolated.sprite.position.y]).toEqual([5.5, 5.5]);
      interpolated.interpolate(20);
      expect([interpolated.sprite.position.x, interpolated.sprite.position.y]).toEqual([6.5, 6.5]);
    });
  });
});

describe('interpolator', () => {
  it('snaps to current location if disabled', () => {
    const pixi = new Application();
    const ticker = pixi.ticker as jest.Mocked<Ticker>;
    const sprite = new Sprite();
    const interpolator = new Interpolator(pixi);

    interpolator.isInterpolationEnabled = false;

    interpolator.new(sprite, { position: [0, 1], velocity: [0, 0] });
    expect(ticker.add).toHaveBeenCalledTimes(1);

    const tickCallback = ticker.add.mock.calls[0][0];
    tickCallback();

    expect([sprite.position.x, sprite.position.y]).toEqual([0, 1]);
  });
});
