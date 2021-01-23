import pytest
import server_interfaces as si
from unittest.mock import Mock
from components import Box2DBody, Position, Velocity
from Box2D import b2Vec2, b2CircleShape
from serializer import short_update_data, long_update_data


@pytest.fixture
def context(empty_context):
    return empty_context


class TestSerializerlong:
    def test_short_update_no_update(self, context):
        assert short_update_data('0', context) == {
            'id': '0',
            'position': None,
            'velocity': None,
        }

    def test_short_update_returns_updated(self, context):
        context.upsert('0',
                       Box2DBody(body=Mock(awake=True, position=(0, 0), fixtures=[])),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert short_update_data('0', context) == {
            'id': '0',
            'position': b2Vec2(0, 0),
            'velocity': b2Vec2(0, 0),
        }


class TestSerializershort:
    def test_long_update_returns_updated(self, context):
        context.upsert('0',
                       Box2DBody(body=Mock(awake=True, position=(0, 0), fixtures=[])),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert long_update_data('0', context) == {
            'id': '0',
            'position': b2Vec2(0, 0),
            'velocity': b2Vec2(0, 0),
            'shape': None
        }

    def test_long_update_serializes_shape(self, context):
        body = Mock(awake=True, position=(1, 2), fixtures=[
            Mock(shape=b2CircleShape(pos=(3, 4), radius=5))
        ])
        context.upsert('0',
                       Box2DBody(body=body),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert long_update_data('0', context)['shape'] == si.ArcShapeData(
            x=3.0,
            y=4.0,
            radius=5,
            start_angle=0,
            end_angle=6.283185307179586,
        )
