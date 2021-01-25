import { si } from './lib';

type ServerEntityData = Partial<si.EntityData & si.ShortEntityData>;
type LocalEntityData = {
};
type Entity = {
  server: ServerEntityData;
  local: LocalEntityData;
};

export class EntityManager {
  public entities: Record<string, Entity> = {};

  public updateEntityShort(id: string, update: Partial<si.ShortEntityData>): void {
    this.updateEntity(id, update);
  }

  public updateEntity(id: string, update: Partial<si.EntityData>): void {
    let entity: Entity;
    if (id in this.entities) {
      entity = this.entities[id];
      Object.assign(entity.server, update);
    } else {
      entity = this.entities[id] = this.newEntity(update);
    }

    if (update?.position) {
      this.updateEntityPosition(entity);
    }
  }

  private newEntity(update: Partial<si.EntityData>): Entity {
    return { server: update, local: { sprites: null } };
  }

  private updateEntityPosition(entity: Entity) {
  }
}
