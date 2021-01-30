from typing import List, Dict, Type, Set, Callable
from ecs.base_system import System, ExternalEvent
from ecs.context import Context
import client_interfaces as ci
import server_interfaces as si
from systems.dependency_graph import resolve_dependency_order
from repository import repository_factory
import serializer
from .exc import GameError


class Game:
    def __init__(self, systems_classes: List[Type[System]], repository_factory: Callable = repository_factory):
        self.systems: Dict[str, List[System]] = {}
        self.contexts: Dict[str, Context] = {}
        self.rooms: Dict[str, si.RoomMeta] = {}
        self._systems_classes = resolve_dependency_order(systems_classes)
        self._repository_factory = repository_factory

    def join_room(
            self,
            sid: str,
            data: ci.JoinRoomDTO,
            callback_enter_room: Callable,
            callback_emit: Callable) -> si.JoinRoomDTO:
        room = self.rooms.get(data.room_id)
        if not room:
            raise GameError('Room does not exist', 404)
        elif len(room.players) >= room.max_players:
            raise GameError('Room is full', 409)
        elif sid in room.players:
            raise GameError('You are already in this room', 400)
        elif self._is_in_a_room(sid):
            raise GameError('You are already in a room', 400)

        room.players.append(sid)
        callback_enter_room(room.id)
        self.trigger_event(ExternalEvent.PLAYER_JOIN, room.id, sid)
        self.sync_full(room.id, sid, callback_emit)

        return si.JoinRoomDTO(room=room)

    def leave_room(self, sid: str, room_id: str):
        room = self.rooms.get(room_id)
        if room and sid in room.players:
            self.trigger_event(ExternalEvent.PLAYER_LEAVE, room_id, sid)
            room.players.remove(sid)
            self.contexts[room_id].remove_entity(sid)
            logging.info(f'{sid} left room {room_id}')

    def get_rooms(self) -> si.GetRoomsDTO:
        rooms = [room for room in self.rooms.values() if not room.private]
        response = si.GetRoomsDTO(rooms=rooms)
        return response

    def create_room(self, sid: str, data: ci.CreateRoomDTO, callback_enter_room: Callable) -> si.CreateRoomDTO:
        if self._is_in_a_room(sid):
            raise GameError('You are already in a room')

        room = self._create_room(data)
        room.players = [sid]

        callback_enter_room(room.id)
        self.trigger_event(ExternalEvent.GAME_INIT, room.id, room)
        self.trigger_event(ExternalEvent.PLAYER_JOIN, room.id, sid)

        return si.CreateRoomDTO(room=room)

    def _create_room(self, data: ci.CreateRoomDTO) -> si.RoomMeta:
        room = si.RoomMeta(id=self._new_id(), players=[], max_players=4, level='beach', **data.__dict__)
        context = Context(repository=self._repository_factory())

        self.rooms[room.id] = room
        self.contexts[room.id] = context
        self.systems[room.id] = [cls(context) for cls in self._systems_classes]
        logging.info('created room')
        return room

    def input(self, sid: str, room_id: str, data: ci.InputDTO):
        self.trigger_event(ExternalEvent.INPUT, room_id, sid, data)

    def trigger_event(self, event: ExternalEvent, room_id: str, *args, **kwargs):
        method_name = f'on_{event.value}'
        for system in self.systems[room_id]:
            try:
                getattr(system, method_name)(*args, **kwargs)
            except NotImplementedError:
                pass

    def update_short(self, dt: float, callback_emit: Callable, sort: bool = False):
        for room_id, context in self.contexts.items():
            self.trigger_event(ExternalEvent.UPDATE_FRAME, room_id, dt)

            updates = serializer.create_short_sync(context, sort)
            callback_emit(updates, room_id)

    def update_long(self, callback_emit: Callable, sort: bool = False):
        for room_id, context in self.contexts.items():
            print(set.union(*context.entities.values()))
            self.trigger_event(ExternalEvent.UPDATE, room_id)

            updates = serializer.create_long_sync(context, sort)
            callback_emit(updates, room_id)

    def sync_full(self, room_id: str, sid: str, callback_emit: Callable, sort: bool = False):
        context = self.contexts[room_id]
        updates = serializer.create_full_sync(context, sort)
        callback_emit(updates, room_id)

    def _get_players(self) -> Set[str]:
        return set(player_id for room in self.rooms.values() for player_id in room.players)

    def _new_id(self) -> str:
        return f'room{len(self.rooms.values())}'

    def _is_in_a_room(self, sid: str):
        return sid in self._get_players()
