import PIXI from 'pixi.js';
import * as lib from '../keyboard';
const ActualKeyboard = jest.requireActual<typeof lib>('../keyboard');
export const { Key } = ActualKeyboard;

export class Keyboard extends ActualKeyboard.Keyboard {
  public eventEmitter = ({ on: jest.fn() } as unknown) as PIXI.utils.EventEmitter;
}
