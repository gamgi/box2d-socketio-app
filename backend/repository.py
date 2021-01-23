from typing import Dict
from typing_extensions import TypedDict
from components import COMPONENTS, Position, Velocity, Box2DWorld, Box2DBody

Repository = TypedDict('Repository', {
    'position': Dict[str, Position],
    'velocity': Dict[str, Velocity],
    'box2d_world': Dict[str, Box2DWorld],
    'box2d_body': Dict[str, Box2DBody],
})


def repository_factory():
    columns = [component.component_name for component in COMPONENTS]
    unique_columns = _validate_columns(columns)
    return Repository({column: dict() for column in unique_columns})  # type: ignore


def _validate_columns(columns):
    unique = set()
    duplicates = set(x for x in columns if x in unique or unique.add(x))  # type: ignore
    if duplicates:
        raise RuntimeError(f'duplicate component fields: {",".join(duplicates)}')
    return unique
