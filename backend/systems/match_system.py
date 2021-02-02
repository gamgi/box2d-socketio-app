from typing import Tuple
from ecs.base_system import System
from ecs.context import Context
from components import Match
from components import Box2DBody, Box2DWorld, Position, Velocity, Angle
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
        for i in range(4):
            self._spawn_box('box' + str(i), (4, -i))

    def _spawn_box(self, entity_id: str, pos: Tuple):
        world = self._get_world()

        box_body = world.CreateDynamicBody(position=pos)
        box_body.CreatePolygonFixture(box=(0.5, 0.5), density=0.2, friction=0.3, restitution=0)
        body = Box2DBody(box_body)

        position = Position.from_body(box_body)
        velocity = Velocity.from_body(box_body)
        collidable = Collidable()
        angle = Angle.Straight()

        self.context.upsert(
            entity_id,
            body,
            position,
            velocity,
            collidable,
            angle
        )

    def _spawn_ball(self, entity_id: str):
        world = self._get_world()

        ball_body = world.CreateDynamicBody(position=(3, 0))
        ball_body.CreateCircleFixture(radius=0.5, density=0.5, friction=0.5)
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
