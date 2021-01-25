import { Application, Container, IResourceDictionary } from 'pixi.js';
import { EntityManager } from './entityManager';
import { si, Client } from './lib';

export class Game {
  public stage: Container = new Container();
  private resources: IResourceDictionary = {};
  private entityManager = new EntityManager();

  constructor(private pixi: Application, private client: Client) {
    pixi.stage.addChild(this.stage);
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
        this.entityManager.updateEntity(update.id, update);
      }
    });

    this.client.eventEmitter.on('short_sync', (data: si.ShortSyncDTO) => {
      for (const update of data.updates) {
        this.entityManager.updateEntityShort(update.id, update);
      }
    });
  }
}
