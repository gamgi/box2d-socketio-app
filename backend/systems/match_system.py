from ecs.base_system import System
from ecs.context import Context
from components import Match
import server_interfaces as si


class MatchSystem(System):

    def __init__(self, context: Context):
        self.context = context

    def on_game_init(self, room: si.RoomMeta):  # type:ignore
        match = Match.Default()
        self.context.new_singleton(match)
