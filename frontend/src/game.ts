import { Application, Container, IResourceDictionary } from 'pixi.js';
import { EntityManager } from './entityManager';
import { si, Client } from './lib';
import { METERS_TO_PX, Y_DIRECTION } from './constants';
import { Vec2 } from './types';
import { isArcShape, isPolygonShape } from './componentUtils';

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
    // eslint-disable-next-line camelcase
    const data = { name, private: isPrivate };
    await this.client.sendOrFailWith<si.CreateRoomDTO>('join_room', data, 'Failed to create room');
  }

  public async joinRoom(roomId: string): Promise<void> {
    // eslint-disable-next-line camelcase
    const data = { room_id: roomId };
    await this.client.sendOrFailWith<si.JoinRoomDTO>('join_room', data, 'Failed to join room');
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

function clientTransformVertex(vector: Vec2): Vec2 {
  return [vector[0] * METERS_TO_PX, vector[1] * METERS_TO_PX];
}

function clientTransformShape(shape: si.EntityData['shape']): si.EntityData['shape'] {
  if (isPolygonShape(shape)) {
    shape.vertices = makeVerticesPositive(shape.vertices as Vec2[]).map(clientTransformVertex);
    shape.x = shape.x * METERS_TO_PX;
    shape.y = shape.y * METERS_TO_PX * Y_DIRECTION;
  } else if (isArcShape(shape)) {
    shape.radius *= METERS_TO_PX;
    shape.x = shape.x * METERS_TO_PX;
    shape.y = shape.y * METERS_TO_PX * Y_DIRECTION;
  }
  return shape;
}

function makeVerticesPositive(vertices: Vec2[]) {
  // Offset vertices so that there are no negative vertices
  // We do this because renderer.generateTexture
  // can't handle negative coordinates for graphic
  const xMin = Math.min(0, ...vertices.flatMap((v) => v[0]));
  const yMin = Math.min(0, ...vertices.flatMap((v) => v[1]));
  return vertices.map((vec) => [vec[0] - xMin, vec[1] - yMin]);
}
