from typing import Union, Dict, cast
from ecs.context import Context
import server_interfaces as si
from Box2D import b2Body, b2Shape, b2CircleShape, b2PolygonShape
from components import Box2DBody, Position, Velocity, Player
from components import SHORT_SYNC_COMPONENTS, LONG_SYNC_COMPONENTS

Shape = Union[si.RectShapeData, si.ArcShapeData]


def create_short_sync(context: Context, sort=False) -> si.ShortSyncDTO:
    if not SHORT_SYNC_COMPONENTS:
        return si.ShortSyncDTO([])

    entity_ids = context.get_updated_entities_for(*SHORT_SYNC_COMPONENTS)
    if sort:
        entity_ids = sorted(entity_ids)  # type: ignore

    updates = [_create_short_sync(entity_id, context) for entity_id in entity_ids]
    return si.ShortSyncDTO(updates)


def create_long_sync(context: Context, sort=False) -> si.LongSyncDTO:
    if not LONG_SYNC_COMPONENTS:
        return si.LongSyncDTO([])

    entity_ids = context.get_updated_entities_for(*LONG_SYNC_COMPONENTS)
    if sort:
        entity_ids = sorted(entity_ids)  # type: ignore

    updates = [_create_long_sync(entity_id, context) for entity_id in entity_ids]
    return si.LongSyncDTO(updates)


def _create_short_sync(entity_id: str, context: Context) -> si.ShortEntityData:
    return si.ShortEntityData(**short_sync_data(entity_id, context))


def _create_long_sync(entity_id: str, context: Context) -> si.EntityData:
    return si.EntityData(**long_sync_data(entity_id, context))


def short_sync_data(entity_id: str, context: Context) -> Dict:
    return {
        'id': entity_id,
        'position': context.get_maybe(entity_id, Position).position,  # type: ignore
        'velocity': context.get_maybe(entity_id, Velocity).velocity,  # type: ignore
    }


def long_sync_data(entity_id: str, context: Context) -> Dict:
    return {
        **short_sync_data(entity_id, context),
        'shape': get_body_shape(context.get_maybe(entity_id, Box2DBody).body),  # type: ignore
        'color': context.get_maybe(entity_id, Player).color,  # type: ignore
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
