import PIXI from 'pixi.js';
import * as lib from '../client';
const MockClient = jest.createMockFromModule<typeof lib>('../client').Client;

export class Client extends MockClient {
  public eventEmitter = ({ on: jest.fn() } as unknown) as PIXI.utils.EventEmitter;
  public connect = jest.fn();
}
