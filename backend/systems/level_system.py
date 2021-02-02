import logging
from typing import Tuple, List
from Box2D import b2Body, b2Vec2
from ecs.base_system import System
from ecs.context import Context
from components import Match
from components import Box2DBody, Box2DWorld, Position, Velocity, Angle, Collidable
import server_interfaces as si
import client_interfaces as ci
from constants import ENTER
from systems.physics_system import PhysicsSystem


class LevelSystem(System):
    requires = [PhysicsSystem]
    bodies: List[b2Body] = []

    def __init__(self, context: Context):
        self.context = context

    def on_game_init(self, room: si.RoomMeta):  # type:ignore
        match = Match.Default()
        self.context.new_singleton(match)
        for i in range(4):
            box_body = self._spawn_box(f'box{i}', (4, -i))
            self.bodies.append(box_body)

    def on_input(self, sid: str, data: ci.InputDTO):
        restart = ENTER in (data.keys_released or [])

        if restart:
            logging.info('restart')
            for i, body in enumerate(self.bodies):
                body.awake = True
                body.angle = 0
                body.position = b2Vec2(4, -i)

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
        return box_body

    def _get_world(self):
        return self.context.singleton(Box2DWorld, field='world')
