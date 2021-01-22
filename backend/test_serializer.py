import pytest
import server_interfaces as si
from unittest.mock import Mock
from components import Box2DBody, Position, Velocity
from Box2D import b2Vec2, b2CircleShape
from serializer import create_fast_sync, create_slow_sync


@pytest.fixture
def context(empty_context):
    return empty_context


class TestSerializerSlow:
    def test_fast_sync_no_update(self, context):
        assert create_fast_sync('0', context) == {
            'id': '0',
            'position': None,
            'velocity': None,
        }

    def test_fast_sync_returns_updated(self, context):
        context.upsert('0',
                       Box2DBody(body=Mock(awake=True, position=(0, 0), fixtures=[])),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert create_fast_sync('0', context) == {
            'id': '0',
            'position': b2Vec2(0, 0),
            'velocity': b2Vec2(0, 0),
        }


class TestSerializerFast:
    def test_slow_sync_returns_updated(self, context):
        context.upsert('0',
                       Box2DBody(body=Mock(awake=True, position=(0, 0), fixtures=[])),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert create_slow_sync('0', context) == {
            'id': '0',
            'position': b2Vec2(0, 0),
            'velocity': b2Vec2(0, 0),
            'shape': None
        }

    def test_slow_sync_serializes_shape(self, context):
        body = Mock(awake=True, position=(1, 2), fixtures=[
            Mock(shape=b2CircleShape(pos=(3, 4), radius=5))
        ])
        context.upsert('0',
                       Box2DBody(body=body),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert create_slow_sync('0', context)['shape'] == si.ArcShapeData(
            x=3.0,
            y=4.0,
            radius=5.0,
            start_angle=0,
            end_angle=6.283185307179586,
        )
