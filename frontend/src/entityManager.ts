import { Application, Container, Sprite, Graphics } from 'pixi.js';
import { si } from './lib';
import { renderGraphicToSprite } from './entityUtils';
import { isPolygonShape } from './componentUtils';

type ServerEntityData = Partial<si.EntityData & si.ShortEntityData>;
type LocalEntityData = {
  sprites: Sprite[];
};
type Entity = {
  server: ServerEntityData;
  local: LocalEntityData;
};

export class EntityManager {
  public entities: Record<string, Entity> = {};

  constructor(private pixi: Application, private stage: Container) {}

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

    if (update?.shape) {
      this.updateEntityShape(entity, update.shape, update?.color ?? 0xffffff);
    }

    if (update?.position) {
      this.updateEntityPosition(entity, update.position);
    }
  }

  public removeEntity(id: string): void {
    if (id in this.entities) {
      const entity = this.entities[id];
      entity.local.sprites.forEach((sprite) => {
        sprite.destroy();
      });
      entity.local.sprites = [];
      delete this.entities[id];
    }
  }

  private newEntity(update: Partial<si.EntityData>): Entity {
    return { server: update, local: { sprites: [] } };
  }

  private updateEntityShape(entity: Entity, shape: si.EntityData['shape'], color: number) {
    if (isPolygonShape(shape)) {
      const graphic = new Graphics().beginFill(color).drawPolygon(shape.vertices.flat()).endFill();
      const sprite = renderGraphicToSprite(graphic, this.pixi);

      entity.local.sprites = [sprite];
      this.stage.addChild(sprite);
      graphic.destroy();
    }
  }

  private updateEntityPosition(entity: Entity, position: si.EntityData['position']) {
    if (entity.local.sprites) {
      entity.local.sprites.forEach((sprite) => {
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        sprite.position.set(position![0], position![1]);
      });
    }
  }
}
