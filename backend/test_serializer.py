import pytest
import server_interfaces as si
from unittest.mock import Mock, ANY
from components import Box2DBody, Position, Velocity
from Box2D import b2Vec2, b2CircleShape
from serializer import short_sync_data, long_sync_data, create_short_sync, create_long_sync


@pytest.fixture
def context(empty_context):
    return empty_context


class TestSerializerShort:
    def test_short_sync_data_no_update(self, context):
        assert short_sync_data('0', context) == {
            'id': '0',
            'position': None,
            'velocity': None,
        }

    def test_short_sync_data_returns_updated(self, context):
        context.upsert('0',
                       Box2DBody(body=Mock(awake=True, position=(0, 0), fixtures=[])),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert short_sync_data('0', context) == {
            'id': '0',
            'position': b2Vec2(0, 0),
            'velocity': b2Vec2(0, 0),
        }

    def test_create_short_sync(self, context):
        context.upsert('0', Position.Origin(), Velocity.Still())
        context.upsert('1', Position.Origin(), Velocity.Still())
        context.get_all_updated_entities(reset=True)

        context.upsert('1', Position.at((0, 1)), Velocity.Still())
        context.upsert('2', Position.Origin(), Velocity.Still())

        assert create_short_sync(context, sort=True) == si.ShortSyncDTO([
            si.ShortEntityData(id='1', position=b2Vec2(0, 1), velocity=b2Vec2(0, 0)),
            si.ShortEntityData(id='2', position=b2Vec2(0, 0), velocity=b2Vec2(0, 0)),
        ])


class TestSerializerLong:
    def test_long_sync_data_returns_updated(self, context):
        context.upsert('0',
                       Box2DBody(body=Mock(awake=True, position=(0, 0), fixtures=[])),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert long_sync_data('0', context) == {
            'id': '0',
            'position': b2Vec2(0, 0),
            'velocity': b2Vec2(0, 0),
            'shape': None,
            'color': None
        }

    def test_long_sync_data_serializes_shape(self, context):
        body = Mock(awake=True, position=(1, 2), fixtures=[
            Mock(shape=b2CircleShape(pos=(3, 4), radius=5))
        ])
        context.upsert('0',
                       Box2DBody(body=body),
                       Position.Origin(),
                       Velocity.Still()
                       )
        assert long_sync_data('0', context)['shape'] == si.ArcShapeData(
            x=3.0, y=4.0,
            radius=5,
            start_angle=ANY,
            end_angle=ANY)

    def test_create_long_sync(self, context):
        context.upsert('0', Position.Origin(), Velocity.Still())
        context.upsert('1', Position.Origin(), Velocity.Still())
        context.get_all_updated_entities(reset=True)

        context.upsert('1', Position.at((0, 1)), Velocity.Still())
        context.upsert('2',
                       Box2DBody(body=Mock(awake=True, position=(0, 0), fixtures=[
                           Mock(shape=b2CircleShape(pos=(3, 4), radius=5))
                       ])),
                       Position.Origin(), Velocity.Still())

        assert create_long_sync(context, sort=True) == si.LongSyncDTO([
            si.EntityData(id='1', position=b2Vec2(0, 1), velocity=b2Vec2(0, 0)),
            si.EntityData(
                id='2',
                position=b2Vec2(0, 0),
                velocity=b2Vec2(0, 0),
                shape=si.ArcShapeData(x=3.0, y=4.0, radius=5, start_angle=ANY, end_angle=ANY)
            )
        ])
