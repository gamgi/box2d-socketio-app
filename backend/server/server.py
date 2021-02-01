from ecs.base_system import ExternalEvent
from typing import Union, Dict, Callable, Optional
from time import time
import logging
import threading
import eventlet
import socketio
from functools import partial
import client_interfaces as ci
from server.decorators import returns_error_dto
from game.game import Game
logging.basicConfig(level=logging.INFO)

TICKS_PER_SECOND = 5


class Server(socketio.Namespace):
    sio: socketio.Server
    game: Game

    def __init__(self, namespace: Union[str, None], sio: socketio.Server, game: Game):
        super().__init__(namespace=namespace)
        self.game = game
        self.sio = sio
        self._last_update: Optional[float] = None

        self.callback_short: Callable = partial(self.sio.emit, 'short_sync')
        self.callback_long: Callable = partial(self.sio.emit, 'long_sync')

    def _init_debug_room(self, name: str):
        room = self.game._create_room(ci.CreateRoomDTO(name, False))
        self.game.trigger_event(ExternalEvent.GAME_INIT, room.id, room)

    def sync(self, shutdown_flag: threading.Event, ticks_per_second):
        frame = 0
        self._init_debug_room('debug room')

        while not shutdown_flag.is_set():
            self.tick(frame == 0)
            self._last_update = time()
            self.sio.sleep(1 / ticks_per_second)
            frame = (frame + 1) % ticks_per_second

    def tick(self, long: bool = True, sort: bool = False):
        if long:
            self.game.update_long(self.callback_long, sort)
        else:
            self.game.update_short(self._get_dt(), self.callback_short, sort)

    @classmethod
    def serve(cls, sio: socketio.Server, app: socketio.WSGIApp, game: Game):
        server = cls(None, sio, game)
        sio.register_namespace(server)

        shutdown_flag = threading.Event()
        sio.start_background_task(server.sync, shutdown_flag, TICKS_PER_SECOND)
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app, log_output=False)
        logging.info('Shutting down')
        shutdown_flag.set()

    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid: str):
        room_id = self._get_room_id(sid)
        if not room_id:
            return
        self.game.leave_room(sid, room_id)

    @returns_error_dto
    def on_get_rooms(self, sid: str, data: None):
        return self.game.get_rooms()

    @returns_error_dto
    def on_join_room(self, sid: str, data: Dict):
        callback = partial(self.sio.enter_room, sid)
        return self.game.join_room(sid, ci.JoinRoomDTO(**data), callback, self.callback_long)

    @returns_error_dto
    def on_create_room(self, sid: str, data: Dict):
        callback = partial(self.sio.enter_room, sid)
        return self.game.create_room(sid, ci.CreateRoomDTO(**data), callback)

    def on_input(self, sid: str, data: Dict):
        room_id = self._get_room_id(sid)
        if not room_id:
            return
        return self.game.input(sid, room_id, ci.InputDTO(**data))

    def _get_dt(self) -> float:
        if self._last_update:
            return time() - self._last_update
        else:
            return 1 / 100

    def _get_room_id(self, sid: str) -> Union[str, None]:
        rooms = set(self.sio.rooms(sid)) - {sid}
        if not rooms:
            return None
        return rooms.pop()  # type: ignore
