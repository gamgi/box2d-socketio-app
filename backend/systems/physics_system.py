from typing import Tuple, Dict
from ecs.base_system import System
from ecs.context import Context
from components import Box2DBody, Box2DWorld, Position, Velocity, Input, Collidable, Angle
from Box2D import b2World, b2EdgeShape, b2Vec2
from constants import BOX2D_VEL_ITERS, BOX2D_POS_ITERS, BodyType


class PhysicsSystem(System):
    def __init__(self, context: Context):
        self.context = context

    def on_game_init(self, room):  # type:ignore
        self._create_world()

    def on_update_frame(self, dt: float):
        world = self._get_world()
        entity_data = self.context.all_dict(
            Box2DBody, optional_components=[Position, Velocity, Input, Collidable, Angle])
        self.do_update(entity_data, world, dt)
        for entity_id, data in entity_data.items():
            body, position, velocity, input, collidable, angle = data
            self._mark_entity_updated(entity_id, body, position, velocity, angle)

    def do_update(self, entity_data: Dict[str, Tuple], world: b2World, dt: float) -> None:
        # flush contactlisteners
        world.Step(0, 0, 0)
        for entity_id, data in entity_data.items():
            body, position, velocity, input, collidable, angle = data
            self._mark_entity_updated(entity_id, body, position, velocity, angle)
            if input:
                self._handle_input(entity_id, body, input, collidable)

        world.Step(dt, BOX2D_VEL_ITERS, BOX2D_POS_ITERS)
        world.ClearForces()

    def _handle_input(self, entity_id: str, body: Box2DBody, input: Input, collidable: Collidable = None):
        if input.move_right:
            body.body.ApplyForceToCenter(b2Vec2(5, 0), True)
        if input.move_left:
            body.body.ApplyForceToCenter(b2Vec2(-5, 0), True)

        # limit x-velocity
        body.body.linearVelocity.x = max(-2, min(body.body.linearVelocity.x, 2))

        if input.jump and collidable and 'floor' in collidable.collides_with:
            body.body.ApplyLinearImpulse(b2Vec2(0, 3), body.body.position, True)

    def _mark_entity_updated(
            self,
            entity_id: str,
            body: Box2DBody,
            position: Position,
            velocity: Velocity,
            angle: Angle):
        if not body.body.awake or body.body.type == BodyType.STATIC:
            return

        if position:
            self.context.mark_entity_updated(entity_id, Position)
        if velocity:
            self.context.mark_entity_updated(entity_id, Velocity)
        if body and angle:
            self.context.component(entity_id, Angle).angle = body.body.angle  # type:ignore
            self.context.mark_entity_updated(entity_id, Angle)

    def _create_world(self):
        world = b2World(gravity=(0, -10), doSleep=True)
        self.context.new_singleton(Box2DWorld(world))

        # left wall
        world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(0, -6), (0, 0)]),
        )
        # right wall
        world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(8, -6), (8, 0)]),
        )

        floor_body = world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(-20, -5.5), (20, -5.5)]),
        )
        self.context.ignore_entity_updates('floor')
        self.context.upsert('floor', Box2DBody(floor_body))

    def _get_world(self):
        return self.context.singleton(Box2DWorld, field='world')
