from typing import Protocol
from abc import abstractmethod
from enum import Enum
from .context import Context

ExternalEvent = Enum('ExternalEvent', ['GAME_INIT', 'INPUT', 'UPDATE', 'UPDATE_FRAME', 'PLAYER_JOIN', 'PLAYER_LEAVE'])


class System(Protocol):
    @abstractmethod
    def __init__(self, context: Context):
        ...

    def on_game_init(self, *args, **kwargs):
        raise NotImplementedError

    def on_input(self, sid: str, data):
        raise NotImplementedError

    def on_update(self):
        raise NotImplementedError

    def on_update_frame(self, dt):
        raise NotImplementedError

    def on_player_join(self, sid: str):
        raise NotImplementedError

    def on_player_leave(self, sid: str):
        raise NotImplementedError
