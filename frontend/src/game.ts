import { Application, Container, IResourceDictionary } from 'pixi.js';
import { EntityManager } from './entityManager';
import { si, Client } from './lib';
import { METERS_TO_PX, Y_DIRECTION } from './constants';
import { Vec2 } from './types';
import { isPolygonShape } from './componentUtils';

export class Game {
  public stage: Container = new Container();
  private resources: IResourceDictionary = {};
  private entityManager: EntityManager;

  constructor(private pixi: Application, private client: Client) {
    pixi.stage.addChild(this.stage);
    this.entityManager = new EntityManager(pixi, this.stage);
    this.initClient();
  }

  public initResources(resources: IResourceDictionary): void {
    this.resources = resources;
  }

  public async createRoom(name: string, isPrivate: boolean): Promise<void> {
    await this.client.createRoom({ name, private: isPrivate });
  }

  private initClient(): void {
    this.client.eventEmitter.on('long_sync', (data: si.LongSyncDTO) => {
      for (const update of data.updates) {
        this.clientTransformUpdateInplace(update);
        this.entityManager.updateEntity(update.id, update);
      }
      data.remove.forEach((id) => this.entityManager.removeEntity(id));
    });

    this.client.eventEmitter.on('short_sync', (data: si.ShortSyncDTO) => {
      for (const update of data.updates) {
        this.clientTransformUpdateInplace(update);
        this.entityManager.updateEntityShort(update.id, update);
      }
      data.remove.forEach((id) => this.entityManager.removeEntity(id));
    });
  }

  private clientTransformUpdateInplace(update: Partial<si.EntityData>): void {
    // transform coordinate system and units from MKS to local game equivalent
    if (update?.position) {
      update.position = clientTransformPosition(update.position as Vec2);
    }
    if (update?.shape) {
      update.shape = clientTransformShape(update.shape);
    }
  }
}

function clientTransformPosition(vector: Vec2): Vec2 {
  return [vector[0] * METERS_TO_PX, vector[1] * METERS_TO_PX * Y_DIRECTION];
}

function clientTransformShape(shape: si.EntityData['shape']): si.EntityData['shape'] {
  if (isPolygonShape(shape)) {
    shape.vertices = (shape.vertices as Vec2[]).map(clientTransformPosition);
    shape.x = shape.x * METERS_TO_PX;
    shape.y = shape.y * METERS_TO_PX * Y_DIRECTION;
  }
  return shape;
}
