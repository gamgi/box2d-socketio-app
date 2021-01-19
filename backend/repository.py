from typing import Dict
from typing_extensions import TypedDict
from components import Position, Velocity, Box2DWorld, Box2DBody

Repository = TypedDict('Repository', {
    'position': Dict[str, Position],
    'velocity': Dict[str, Velocity],
    'box2d_world': Dict[str, Box2DWorld],
    'box2d_body': Dict[str, Box2DBody],
})
