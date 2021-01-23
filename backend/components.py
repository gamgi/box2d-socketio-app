from typing import Sequence, List
from dataclasses import dataclass, is_dataclass
from Box2D import b2World, b2Body, b2Vec2
from constants import MatchState
from ecs.base_component import Component


@dataclass
class Position(Component):
    component_name = 'position'
    position: b2Vec2

    @classmethod
    def Origin(cls):
        return cls(position=b2Vec2(0, 0))

    @classmethod
    def at(cls, values: Sequence):
        return cls(position=b2Vec2(values))

    @classmethod
    def from_body(cls, body: b2Body):
        return cls(position=body.position)


@dataclass
class Velocity(Component):
    component_name = 'velocity'
    velocity: b2Vec2

    @classmethod
    def Still(cls):
        return cls(velocity=b2Vec2((0, 0)))

    @classmethod
    def from_body(cls, body: b2Body):
        return cls(velocity=body.linearVelocity)


@dataclass
class Box2DWorld(Component):
    component_name = 'box2d_world'
    world: b2World


@dataclass
class Box2DBody(Component):
    component_name = 'box2d_body'
    body: b2Body

    def __register_entity__(self, entity_id: str):
        self.body.userData = entity_id


@dataclass
class Player(Component):
    component_name = 'player'
    color: str


@dataclass
class Team(Component):
    component_name = 'team'
    index: int


@dataclass
class Match(Component):
    component_name = 'match'
    state: MatchState
    teams: List[int]

    @classmethod
    def Default(cls):
        return cls(state=MatchState.NOT_STARTED, teams=[0, 1])


COMPONENTS = list(filter(lambda cls: is_dataclass(cls) and issubclass(cls, Component), locals().values()))
