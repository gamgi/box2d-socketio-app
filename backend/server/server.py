from typing import Union, Dict
import logging
import threading
import eventlet
import socketio
from functools import partial
import client_interfaces as ci
from server.decorators import returns_error_dto
from game.game import Game
logging.basicConfig(level=logging.INFO)

TICKS_PER_SECOND = 2


class Server(socketio.Namespace):
    sio: socketio.Server
    game: Game

    def __init__(self, namespace: Union[str, None], sio: socketio.Server, game: Game):
        super().__init__(namespace=namespace)
        self.game = game
        self.sio = sio
        self._last_update = None

    @classmethod
    def serve(cls, sio: socketio.Server, app: socketio.WSGIApp, game: Game):
        server = cls(None, sio, game)
        sio.register_namespace(server)

        shutdown_flag = threading.Event()
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

        shutdown_flag.set()

    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass

    @returns_error_dto
    def on_get_rooms(self, sid: str, data: None):
        return self.game.get_rooms()

    @returns_error_dto
    def on_join_room(self, sid: str, data: Dict):
        callback = partial(self.sio.enter_room, sid)
        return self.game.join_room(sid, ci.JoinRoomDTO(**data), callback)

    @returns_error_dto
    def on_create_room(self, sid: str, data: Dict):
        callback = partial(self.sio.enter_room, sid)
        return self.game.create_room(sid, ci.CreateRoomDTO(**data), callback)
