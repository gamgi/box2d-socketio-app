import { si } from './lib';

export function isPolygonShape(shape: si.EntityData['shape']): shape is si.PolygonShapeData {
  return shape?.form === 'polygon';
}

export function isArcShape(shape: si.EntityData['shape']): shape is si.ArcShapeData {
  return shape?.form === 'arc';
}