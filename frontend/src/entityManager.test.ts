import { EntityManager } from './entityManager';

describe('EntityManager', () => {
  it('updateEntity creates new entity if not found', () => {
    const manager = new EntityManager();
    const entityData = { id: '0', position: [0, 1], velocity: [2, 3] };
    manager.updateEntity('0', entityData);

    expect(manager.entities['0']).toEqual({
      local: expect.any(Object),
      server: entityData,
    });
  });

  it('updateEntity updates entity', () => {
    const manager = new EntityManager();
    const entityData = { id: '0', position: [0, 1], velocity: [2, 3] };
    manager.updateEntity('0', entityData);
    manager.updateEntity('0', { velocity: [4, 5] });

    expect(manager.entities['0'].server.velocity).toEqual([4, 5]);
  });
});
