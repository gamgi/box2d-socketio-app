import { Sprite } from 'pixi.js';
import { EntityManager } from './entityManager';
import { si } from './lib';

describe('EntityManager', () => {
  const mockPixi = { renderer: { render: jest.fn() } } as any;
  const mockStage = { addChild: () => {} } as any;
  const entityWithShape: Partial<si.EntityData> = {
    shape: {
      x: 0,
      y: 0,
      // eslint-disable-next-line prettier/prettier
      vertices: [ [-1, -1], [1, -1], [1, 1], [-1, 1] ] as any,
      fill: true,
      form: 'polygon',
    },
  };

  it('updateEntity creates new entity if not found', () => {
    const manager = new EntityManager(jest.fn() as any, jest.fn() as any);
    const entityData = { id: '0', position: [0, 1], velocity: [2, 3] };
    manager.updateEntity('0', entityData);

    expect(manager.entities['0']).toEqual({
      local: expect.any(Object),
      server: entityData,
    });
  });

  it('updateEntity updates entity server data', () => {
    const manager = new EntityManager(jest.fn() as any, jest.fn() as any);
    const entityData = { id: '0', position: [0, 1], velocity: [2, 3] };
    manager.updateEntity('0', entityData);
    manager.updateEntity('0', { velocity: [4, 5] });

    expect(manager.entities['0'].server.velocity).toEqual([4, 5]);
  });

  it('updateEntity updates entity shape', () => {
    const manager = new EntityManager(mockPixi, mockStage);
    const shape: si.PolygonShapeData = {
      x: 0,
      y: 0,
      // eslint-disable-next-line prettier/prettier
      vertices: [ [-1, -1], [1, -1], [1, 1], [-1, 1] ] as any,
      fill: true,
      form: 'polygon',
    };
    manager.updateEntity('0', { id: '0', shape });

    expect(manager.entities['0'].local.sprites[0]).toBeInstanceOf(Sprite);
  });

  it('updateEntity updates entity position', () => {
    const manager = new EntityManager(mockPixi, mockStage);
    manager.updateEntity('0', { ...entityWithShape, id: '0', position: [0, 1] });
    const position = manager.entities['0'].local.sprites[0].getGlobalPosition();

    expect(position).toEqual({ x: 0, y: 1 });
  });
});
