import { Vec2 } from './lib';

export const coalesceVec2 = (...vectors: Array<Vec2 | number[] | null | undefined>): Vec2 => {
  // get first nonzero vector, or a zero vector
  const nonzero = vectors.filter((vec) => vec != null && vec.length === 2 && (vec[0] !== 0 || vec[1] !== 0)) as Vec2[];
  return nonzero.pop() ?? [0, 0];
};
