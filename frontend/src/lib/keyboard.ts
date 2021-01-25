import { utils } from 'pixi.js';

export enum Key {
  ArrowLeft = 'ArrowLeft',
  ArrowRight = 'ArrowRight',
  ArrowUp = 'ArrowUp',
  ArrowDown = 'ArrowDown',
  Enter = 'Enter',
  ControlLeft = 'ControlLeft',
  AltLeft = 'AltLeft',
  KeyZ = 'KeyZ',
}

export enum Action {
  MoveUp = 'MoveUp',
  MoveDown = 'MoveDown',
  MoveLeft = 'MoveLeft',
  MoveRight = 'MoveRight',
}

export interface KeyboardContext {
  keysDown: string[];
}

type Controls = {
  [action in Action]: Key;
};

interface KeyboardOptions {
  controls: Controls;
}

const defaultControls: Controls = {
  MoveUp: Key.ArrowUp,
  MoveDown: Key.ArrowDown,
  MoveLeft: Key.ArrowLeft,
  MoveRight: Key.ArrowRight,
};

export class Keyboard {
  private keysDown: string[] = [];
  public eventEmitter: utils.EventEmitter;
  private listenKeys: string[];
  private options: KeyboardOptions;

  constructor(options?: Partial<KeyboardOptions>) {
    window.addEventListener('keydown', this.onKeyDown.bind(this));
    window.addEventListener('keyup', this.onKeyUp.bind(this));

    this.options = {
      ...options,
      controls: defaultControls,
    };

    this.listenKeys = Object.values(this.options.controls);
    this.eventEmitter = new utils.EventEmitter();
  }

  private get context(): KeyboardContext {
    return { keysDown: this.keysDown };
  }

  private onKeyDown(e: KeyboardEvent) {
    const key = e.code;
    if (!this.listenKeys.includes(key)) {
      return;
    }
    if (!this.keysDown.includes(key)) {
      this.keysDown.push(key);
      this.eventEmitter.emit('pressed', key, this.context);
    }
  }

  private onKeyUp(e: KeyboardEvent) {
    const key = e.code;
    if (!this.listenKeys.includes(key)) {
      return;
    }
    if (this.keysDown.includes(key)) {
      this.removeKeyDown(key);
      this.eventEmitter.emit('released', key, this.context);
    }
  }

  private removeKeyDown(key: string) {
    this.keysDown.forEach((item: string, index: number) => {
      if (item === key) this.keysDown.splice(index, 1);
    });
  }
}
