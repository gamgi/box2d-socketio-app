from typing import Protocol
from abc import abstractmethod
from enum import Enum
from .context import Context


class ExternalEvent(Enum):
    GAME_INIT = 'game_init'
    INPUT = 'input'
    UPDATE = 'update'
    UPDATE_FRAME = 'update_frame'
    PLAYER_JOIN = 'player_join'
    PLAYER_LEAVE = 'player_leave'


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
