import pytest
from physics_system import PhysicsSystem
from unittest.mock import patch, Mock
from components import Box2DWorld


@pytest.fixture
def context(empty_context):
    return empty_context


@pytest.fixture
def system(context):
    system = PhysicsSystem(context)
    return system


class TestPhysicsSystem:
    def test_on_game_init_creates_world(self, system, context):
        system.on_game_init(None)
        assert context.get_singleton(Box2DWorld)

    def test_on_update_frame_calls_step(self, system):
        world = Mock(bodies_gen=[])
        with patch('physics_system.b2World', return_value=world):
            system.on_game_init(None)
            system.on_update_frame(1)
        world.Step.assert_called_once()
