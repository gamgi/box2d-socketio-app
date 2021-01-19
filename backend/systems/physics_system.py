from typing import List, Tuple
from ecs.base_system import System
from ecs.context import Context
from components import Box2DBody, Box2DWorld, Position, Velocity
from Box2D import b2World, b2EdgeShape

BOX2D_SETTINGS = {
    'vel_iters': 6,
    'pos_iters': 2
}


class PhysicsSystem(System):
    def __init__(self, context: Context):
        self.context = context

    def on_game_init(self, room):  # type:ignore
        self._create_world()

    def on_update_frame(self, dt: float):
        world = self.context.get_singleton(Box2DWorld, field='world')
        entity_data = self.context.all_dict(Box2DBody, optional_components=[Position, Velocity])
        self.do_update(entity_data, world, dt)

    def do_update(self, entity_data: List[Tuple], world: b2World, dt: float) -> None:
        world.Step(dt, BOX2D_SETTINGS['vel_iters'], BOX2D_SETTINGS['pos_iters'])
        world.ClearForces()

    def _create_world(self):
        world = b2World(gravity=(0, -10), doSleep=True)
        self.context.new_singleton(Box2DWorld(world))

        # ground
        world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(-20, -4), (20, -4)]),
            userData='floor'
        )
