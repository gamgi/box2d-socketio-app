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
});
