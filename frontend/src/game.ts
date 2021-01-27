import { Application, Container, IResourceDictionary } from 'pixi.js';
import { EntityManager } from './entityManager';
import { si, Client } from './lib';
import { METERS_TO_PX, Y_DIRECTION } from './constants';
import { isPolygonShape } from './componentUtils';

type Vec = [number, number];

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

  private clientTransformUpdateInplace(update: si.EntityData | si.ShortEntityData): void {
    // transform coordinate system and units from MKS to local game equivalent
    if ('position' in update) {
      update.position = clientTransformVec(update.position as Vec);
    }
    if ('shape' in update) {
      update.shape = clientTransformShape(update.shape);
    }
  }
}

function clientTransformVec(vector: Vec): Vec {
  return [vector[0] * METERS_TO_PX, vector[1] * METERS_TO_PX * Y_DIRECTION];
}

function clientTransformShape(shape: si.EntityData['shape']): si.EntityData['shape'] {
  if (isPolygonShape(shape)) {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    shape.vertices = (shape.vertices as Vec[]).map(clientTransformVec) as Array<[number]>;
    shape.x = shape.x * METERS_TO_PX;
    shape.y = shape.y * METERS_TO_PX * Y_DIRECTION;
  }
  return shape;
}
