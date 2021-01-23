import pytest
from physics_system import PhysicsSystem
from unittest.mock import patch, Mock
from components import Box2DWorld, Box2DBody, Position, Velocity


@pytest.fixture
def context(empty_context):
    return empty_context


@pytest.fixture
def system(context):
    return PhysicsSystem(context)


class TestPhysicsSystem:
    def test_on_game_init_creates_world(self, system, context):
        system.on_game_init(None)
        assert context.singleton(Box2DWorld)

    def test_on_update_frame_calls_step(self, system):
        world = Mock(bodies_gen=[])
        with patch('physics_system.b2World', return_value=world):
            system.on_game_init(None)
            system.on_update_frame(1)
        world.Step.assert_called_once()

    def test_on_update_frame_marks_all_awake_entities_updated(self, system, context):
        context.upsert('0',
                       Box2DBody(body=Mock(awake=True, position=(0, 0))),
                       Position.Origin(),
                       Velocity.Still()
                       )

        context.upsert('1',
                       Box2DBody(body=Mock(awake=False, position=(0, 0))),
                       Position.Origin(),
                       Velocity.Still()
                       )
        context.get_all_updated_entities(reset=True)

        system.on_game_init(None)
        system.on_update_frame(1)

        updated_entities = context.get_all_updated_entities()
        assert '0' in updated_entities
        assert '1' not in updated_entities