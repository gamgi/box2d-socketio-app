from ecs.base_system import System
from ecs.context import Context
from components import Match
from components import Box2DBody, Box2DWorld, Position, Velocity
from components import Ball, Collidable
import server_interfaces as si
from systems.player_system import PlayerSystem


class MatchSystem(System):
    requires = [PlayerSystem]

    def __init__(self, context: Context):
        self.context = context

    def on_game_init(self, room: si.RoomMeta):  # type:ignore
        match = Match.Default()
        self.context.new_singleton(match)
        self._spawn_ball('ball')

    def _spawn_ball(self, entity_id: str):
        world = self._get_world()

        ball_body = world.CreateDynamicBody(position=(2, 0))
        ball_body.CreateCircleFixture(radius=0.5, density=0.5, friction=0.5, restitution=0.5)
        body = Box2DBody(ball_body)
        collidable = Collidable()

        position = Position.from_body(ball_body)
        velocity = Velocity.from_body(ball_body)
        ball = Ball()

        self.context.upsert(
            entity_id,
            body,
            position,
            velocity,
            ball,
            collidable
        )

    def _get_world(self):
        return self.context.singleton(Box2DWorld, field='world')
