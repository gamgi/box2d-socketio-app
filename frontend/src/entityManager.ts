import { Application, Container, Sprite, Graphics, SCALE_MODES } from 'pixi.js';
import { si, Interpolator, Vec2, Spline, InterpolationData, InterpolatedSprite } from './lib';
import { renderGraphicToSprite } from './entityUtils';
import { isPolygonShape, isArcShape } from './componentUtils';

type ServerEntityData = Partial<si.EntityData & si.ShortEntityData>;
type LocalEntityData = {
  sprites: Sprite[];
  interpolated?: InterpolatedSprite;
};
type Entity = {
  server: ServerEntityData;
  local: LocalEntityData;
};

export class EntityManager {
  public entities: Record<string, Entity> = {};
  private interpolator: Interpolator;

  constructor(private pixi: Application, private stage: Container) {
    this.interpolator = new Interpolator(pixi);
  }

  public onReceiveData(): void {
    this.interpolator.onReceiveData();
  }

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

    if (update?.shape) {
      this.initializeEntityInterpolation(
        entity,
        entity.local.sprites,
        (update?.position ?? entity?.server?.position ?? [0, 0]) as Vec2,
        (update?.velocity ?? entity?.server?.velocity ?? [0, 0]) as Vec2,
      );
    } else if (update?.position && entity.local.interpolated) {
      this.updateEntityInterpolation(
        entity,
        (update?.position ?? entity?.server?.position ?? [0, 0]) as Vec2,
        (update?.velocity ?? entity?.server?.velocity ?? [0, 0]) as Vec2,
      );
    }

    if (update?.angle) {
      this.updateEntityAngle(entity, update.angle);
    }
  }

  public removeEntity(id: string): void {
    if (id in this.entities) {
      const entity = this.entities[id];
      this.removeEntitySprites(entity);
      delete this.entities[id];
    }
  }

  private removeEntitySprites(entity: Entity): void {
    entity.local.sprites.forEach((sprite) => {
      sprite.destroy();
    });
    entity.local.sprites = [];
  }

  private newEntity(update: Partial<si.EntityData>): Entity {
    return { server: update, local: { sprites: [] } };
  }

  private updateEntityShape(entity: Entity, shape: si.EntityData['shape'], color: number) {
    if (isPolygonShape(shape)) {
      this.removeEntitySprites(entity);

      const graphic = new Graphics().beginFill(color).drawPolygon(shape.vertices.flat()).endFill();
      const sprite = renderGraphicToSprite(graphic, this.pixi);
      sprite.pivot.set(graphic.width / 2, graphic.height / 2);

      entity.local.sprites = [sprite];
      this.stage.addChild(sprite);
      graphic.destroy();
    } else if (isArcShape(shape)) {
      this.removeEntitySprites(entity);

      const graphic = new Graphics()
        .beginFill(color)
        .arc(shape.x + shape.radius, shape.y + shape.radius, shape.radius, shape.start_angle, shape.end_angle)
        .endFill();
      const sprite = renderGraphicToSprite(graphic, this.pixi);
      sprite.pivot.set(shape.radius);

      entity.local.sprites = [sprite];
      this.stage.addChild(sprite);
      graphic.destroy();
    }
  }

  private updateEntityAngle(entity: Entity, angle: number) {
    entity.local.sprites.forEach((sprite) => {
      sprite.rotation = angle;
    });
  }

  private updateEntityPosition(entity: Entity, position: si.EntityData['position']) {
    if (entity.local.sprites) {
      entity.local.sprites.forEach((sprite) => {
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        sprite.position.set(position![0], position![1]);
      });
    }
  }

  private initializeEntityInterpolation(entity: Entity, sprites: Sprite[], position: Vec2, velocity: Vec2) {
    if (!entity.local.interpolated) {
      entity.local.interpolated = this.interpolator.new(sprites[0], { position, velocity });
    } else {
      entity.local.interpolated.sprite = sprites[0];
    }
  }

  private updateEntityInterpolation(entity: Entity, position: Vec2, velocity: Vec2) {
    if (!entity?.local?.interpolated) {
      return;
    }

    const { serverDeltaTime, localDeltaFrames } = this.interpolator.getInterpolationData();
    entity.local.interpolated.recalculateInterpolation({ position, velocity }, serverDeltaTime, localDeltaFrames);
  }
}
