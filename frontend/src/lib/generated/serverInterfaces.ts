/* eslint-disable @typescript-eslint/array-type */
/* eslint-disable camelcase */
// Generated using py-ts-interfaces.
// See https://github.com/cs-cordero/py-ts-interfaces

export interface RoomMeta {
  id: string;
  name: string;
  players: Array<string>;
  max_players: number;
  private: boolean;
  level: string;
}

export interface GetRoomsDTO {
  rooms: Array<RoomMeta>;
}

export interface CreateRoomDTO {
  room: RoomMeta;
}

export interface JoinRoomDTO {
  room: RoomMeta;
}

export interface RectShapeData {
  x: number;
  y: number;
  width: number;
  height: number;
  fill: boolean;
  form: string;
}

export interface ArcShapeData {
  x: number;
  y: number;
  radius: number;
  start_angle: number;
  end_angle: number;
  fill: boolean;
  form: string;
}

export interface PolygonShapeData {
  x: number;
  y: number;
  vertices: Array<[number]>;
  fill: boolean;
  form: string;
}

export interface ShortEntityData {
  id: string;
  position: Array<number> | null;
  velocity: Array<number> | null;
}

export interface EntityData {
  id: string;
  position: Array<number> | null;
  velocity: Array<number> | null;
  shape: PolygonShapeData | ArcShapeData | RectShapeData | null;
  color: number | null;
}

export interface ShortSyncDTO {
  updates: Array<ShortEntityData>;
  remove: Array<string>;
}

export interface LongSyncDTO {
  updates: Array<EntityData>;
  remove: Array<string>;
}

export interface ErrorDTO {
  error: boolean;
  code: number;
  message: string;
}