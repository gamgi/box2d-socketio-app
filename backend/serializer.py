from typing import Union, Dict
from ecs.context import Context
import server_interfaces as si
from Box2D import b2Shape, b2CircleShape, b2PolygonShape
from components import Box2DBody, Position, Velocity

Shape = Union[si.RectShapeData, si.ArcShapeData]


def create_fast_sync(entity_id: str, context: Context) -> Dict:
    return {
        'id': entity_id,
        'position': context.get_maybe(entity_id, Position).position,
        'velocity': context.get_maybe(entity_id, Velocity).velocity,
    }


def create_slow_sync(entity_id: str, context: Context) -> Dict:
    return {
        **create_fast_sync(entity_id, context),
        'shape': get_body_shape(context.get_maybe(entity_id, Box2DBody).body)
    }


def get_body_shape(body: Union[Box2DBody, None]) -> Union[Shape, None]:
    if body is None or len(body.fixtures) == 0:
        return
    shape = body.fixtures[0].shape

    return serialize_b2Shape(shape)


def serialize_b2Shape(shape: b2Shape) -> Union[Shape, None]:
    if isinstance(shape, b2CircleShape):
        return si.ArcShapeData.from_b2Circlehape(shape)

    if isinstance(shape, b2PolygonShape):
        return si.PolygonShapeData.from_b2PolygonShape(shape)

    return None
