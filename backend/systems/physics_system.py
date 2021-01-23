from typing import Tuple, Dict
from ecs.base_system import System
from ecs.context import Context
from components import Box2DBody, Box2DWorld, Position, Velocity, Input
from Box2D import b2World, b2EdgeShape, b2Vec2
from constants import BOX2D_VEL_ITERS, BOX2D_POS_ITERS


class PhysicsSystem(System):
    def __init__(self, context: Context):
        self.context = context

    def on_game_init(self, room):  # type:ignore
        self._create_world()

    def on_update_frame(self, dt: float):
        world = self._get_world()
        entity_data = self.context.all_dict(Box2DBody, optional_components=[Position, Velocity, Input])
        self.do_update(entity_data, world, dt)
        for entity_id, data in entity_data.items():
            body, position, velocity, input = data
            self._mark_entity_updated(entity_id, body, position, velocity)

    def do_update(self, entity_data: Dict[str, Tuple], world: b2World, dt: float) -> None:
        for entity_id, data in entity_data.items():
            body, position, velocity, input = data
            self._mark_entity_updated(entity_id, body, position, velocity)
            self._handle_input(entity_id, input, body)

        world.Step(dt, BOX2D_VEL_ITERS, BOX2D_POS_ITERS)
        world.ClearForces()

    def _handle_input(self, entity_id: str, input: Input, body: Box2DBody):
        if input.move_right:
            body.body.ApplyForceToCenter(b2Vec2(50, 0), True)
        if input.move_left:
            body.body.ApplyForceToCenter(b2Vec2(-50, 0), True)

    def _mark_entity_updated(self, entity_id: str, body: Box2DBody, position: Position, velocity: Velocity):
        if not body.body.awake:
            return

        if position:
            self.context.mark_entity_updated(entity_id, Position)
        if velocity:
            self.context.mark_entity_updated(entity_id, Velocity)

    def _create_world(self):
        world = b2World(gravity=(0, -10), doSleep=True)
        self.context.new_singleton(Box2DWorld(world))

        # ground
        world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(-20, -4), (20, -4)]),
            userData='floor'
        )

    def _get_world(self):
        return self.context.singleton(Box2DWorld, field='world')
