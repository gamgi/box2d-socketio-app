from typing import Union, Dict, cast
from ecs.context import Context
import server_interfaces as si
from Box2D import b2Body, b2Shape, b2CircleShape, b2PolygonShape
from components import Box2DBody, Position, Velocity

Shape = Union[si.RectShapeData, si.ArcShapeData]


def create_short_sync(entity_id: str, context: Context) -> si.ShortEntityData:
    return si.ShortEntityData(**short_sync_data(entity_id, context))


def short_sync_data(entity_id: str, context: Context) -> Dict:
    return {
        'id': entity_id,
        'position': context.get_maybe(entity_id, Position).position,  # type:ignore
        'velocity': context.get_maybe(entity_id, Velocity).velocity,  # type:ignore
    }


def create_long_sync(entity_id: str, context: Context) -> si.EntityData:
    return si.EntityData(**short_sync_data(entity_id, context))


def long_sync_data(entity_id: str, context: Context) -> Dict:
    return {
        **short_sync_data(entity_id, context),
        'shape': get_body_shape(context.get_maybe(entity_id, Box2DBody).body)  # type:ignore
    }


def get_body_shape(body: Union[b2Body, None]) -> Union[Shape, None]:
    if body is None or len(body.fixtures) == 0:
        return None
    shape = body.fixtures[0].shape

    return serialize_b2Shape(shape)


def serialize_b2Shape(shape: b2Shape) -> Union[Shape, None]:
    if isinstance(shape, b2CircleShape):
        return cast(si.ArcShapeData, si.ArcShapeData.from_b2Circlehape(shape))

    if isinstance(shape, b2PolygonShape):
        return cast(si.PolygonShapeData, si.PolygonShapeData.from_b2PolygonShape(shape))

    return None
