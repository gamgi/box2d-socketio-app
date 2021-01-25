/* eslint-disable @typescript-eslint/array-type */
/* eslint-disable camelcase */
// Generated using py-ts-interfaces.
// See https://github.com/cs-cordero/py-ts-interfaces

export interface CreateRoomDTO {
  name: string;
  private: boolean;
}

export interface JoinRoomDTO {
  room_id: string;
}

export interface InputDTO {
  keys_down: Array<string>;
  keys_pressed: Array<string> | null;
  keys_released: Array<string> | null;
}