import { Vec2 } from './types';
import { createLinear, createSpline, evalSpline, Spline } from './spline';

describe('createSpline', () => {
  it('sets c1 and c4 as start and end position', () => {
    const startPosition: Vec2 = [1, 1];
    const endPosition: Vec2 = [3, 3];
    const velocity: Vec2 = [0, 0];
    const spline = createSpline(startPosition, velocity, endPosition, velocity, 1);

    expect(spline.d).toEqual(startPosition);

    expect(spline.a).toEqual([
      // nontrivial values
      2 * (startPosition[0] - endPosition[0]),
      2 * (startPosition[1] - endPosition[1]),
    ]);
  });
});

describe('evalSpline', () => {
  it('evaluates trivial spline t=0 as start position', () => {
    const startPosition = [1, 1];
    const spline: Spline = { a: [0, 0], b: [0, 0], c: [0, 0], d: startPosition };

    expect(evalSpline(spline, 0)).toEqual(startPosition);
  });

  it('evaluates trivial spline t=1 as end position', () => {
    const startPosition = [1, 1];
    const endPosition = [2, 2];
    const a = [endPosition[0] - startPosition[0], endPosition[1] - startPosition[1]];
    const spline: Spline = { a, b: [0, 0], c: [0, 0], d: startPosition };

    expect(evalSpline(spline, 1)).toEqual(endPosition);
  });
});

describe('evalSpline and createSpline', () => {
  it('evaluating created spline returns original values', () => {
    const startPosition: Vec2 = [1, 1];
    const endPosition: Vec2 = [2, 3];
    const velocity: Vec2 = [0, 0];
    const spline = createSpline(startPosition, velocity, endPosition, velocity, 1);
    expect(evalSpline(spline, 0)).toEqual(startPosition);
    expect(evalSpline(spline, 1)).toEqual(endPosition);
  });

  it('estimates ends position based on enbd velocity and lapsed frames', () => {
    const startPosition: Vec2 = [1, 1];
    const endPosition: Vec2 = [4, 4];
    const startVelocity: Vec2 = [0, 0];
    const endVelocity: Vec2 = [1, 0];
    const frames = 3;
    const spline = createSpline(startPosition, startVelocity, endPosition, endVelocity, frames);

    expect(evalSpline(spline, 0)).toEqual(startPosition);
    expect(evalSpline(spline, 1)).toEqual([
      endPosition[0] + endVelocity[0] * frames,
      endPosition[1] + endVelocity[1] * frames,
    ]);
  });

  it('evaluates trivial t=1/2 as middle point', () => {
    const startPosition: Vec2 = [0, 0];
    const endPosition: Vec2 = [4, 0];
    const startVelocity: Vec2 = [1, 0];
    const endVelocity: Vec2 = [1, 0];
    const spline = createSpline(startPosition, startVelocity, endPosition, endVelocity, 1);

    expect(evalSpline(spline, 0.5)).toEqual([2.5, 0]);
  });
});

describe('createLinear', () => {
  it('creates linear extrapolation from position', () => {
    const startPosition: Vec2 = [1, 1];
    const velocity: Vec2 = [0, 0];
    const line = createLinear(startPosition, velocity, 1);

    expect(line.d).toEqual(startPosition);
    expect(line.c).toEqual(velocity);
  });

  it('linear extrapolation start matches spline end', () => {
    const startPosition: Vec2 = [1, 1];
    const endPosition: Vec2 = [3, 3];
    const velocity: Vec2 = [1, 1];
    const spline = createSpline(startPosition, velocity, endPosition, velocity, 1);
    const line = createLinear(endPosition, velocity, 1);
    expect(evalSpline(spline, 1)).toEqual([4, 4]);
    expect(evalSpline(line, 0)).toEqual([4, 4]);
  });

  it('linear extrapolation works', () => {
    const startPosition: Vec2 = [1, 1];
    const velocity: Vec2 = [1, 2];
    const line = createLinear(startPosition, velocity, 1);
    expect(evalSpline(line, 0)).toEqual([2, 3]);
    expect(evalSpline(line, 1)).toEqual([3, 5]);
  });
});
