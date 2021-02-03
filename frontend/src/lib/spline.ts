import { Vec2 } from './types';

export type Spline = {
  a: Vec2;
  b: Vec2;
  c: Vec2;
  d: Vec2;
};

export function createLinear(position: Vec2, velocity: Vec2, deltaTime: number, vc = 1): Spline {
  const t = deltaTime;
  return {
    a: [0, 0],
    b: [0, 0],
    c: [velocity[0] * vc, velocity[1] * vc],
    d: [position[0] + velocity[0] * t * vc, position[1] + velocity[1] * t * vc],
  };
}

export function createSpline(
  oldPosition: Vec2,
  oldVelocity: Vec2,
  newPosition: Vec2,
  newVelocity: Vec2,
  deltaTime: number,
  vc = 1,
): Spline {
  const t = deltaTime;
  // spline coordinates
  const c1 = oldPosition; // current position with old data
  const c2 = [
    // new position with old data
    oldPosition[0] + oldVelocity[0] * t * vc,
    oldPosition[1] + oldVelocity[1] * t * vc,
  ];
  const c4 = [
    // new position with new data
    newPosition[0] + newVelocity[0] * t * vc,
    newPosition[1] + newVelocity[1] * t * vc,
  ];
  const c3 = [
    // current position with new data
    newPosition[0],
    newPosition[1],
  ];
  // spline constants
  const a: Vec2 = [
    c4[0] - 3 * c3[0] + 3 * c2[0] - c1[0], // A
    c4[1] - 3 * c3[1] + 3 * c2[1] - c1[1], // E
  ];
  const b: Vec2 = [
    3 * c3[0] - 6 * c2[0] + 3 * c1[0], // B
    3 * c3[1] - 6 * c2[1] + 3 * c1[1], // F
  ];
  const c: Vec2 = [
    3 * c2[0] - 3 * c1[0], // C
    3 * c2[1] - 3 * c1[1], // G
  ];
  const d = c1;

  return { a, b, c, d };
}

export function evalSpline(spline: Spline, t: number): Vec2 {
  const x = spline.a[0] * t ** 3 + spline.b[0] * t ** 2 + spline.c[0] * t + spline.d[0];
  const y = spline.a[1] * t ** 3 + spline.b[1] * t ** 2 + spline.c[1] * t + spline.d[1];
  return [x, y];
}

const PI = Math.PI;
const twoPI = 2 * Math.PI;
const threePI = 3 * Math.PI;

export const evalAngle = (start: number, end: number, t: number): number => {
  // https://stackoverflow.com/questions/2708476/rotation-interpolation
  const shortestAngle = ((((end - start) % twoPI) + threePI) % twoPI) - PI;
  return start + ((shortestAngle * t) % twoPI);
};
