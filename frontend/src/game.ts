import { Application, Container, IResourceDictionary } from 'pixi.js';
import { Client } from './lib';

export class Game {
  public stage: Container = new Container();
  private resources: IResourceDictionary = {};

  constructor(private pixi: Application, private client: Client) {
    pixi.stage.addChild(this.stage);
    this.initClient();
  }

  public initResources(resources: IResourceDictionary): void {
    this.resources = resources;
  }

  // eslint-disable-next-line @typescript-eslint/no-empty-function
  private initClient(): void {}
}
