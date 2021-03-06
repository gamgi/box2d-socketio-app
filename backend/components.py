from typing import Sequence, List, Set
from dataclasses import dataclass, is_dataclass, field
from Box2D import b2World, b2Body, b2Vec2
from constants import MatchState
from ecs.base_component import Component, Sync


@dataclass
class Position(Component):
    component_name = 'position'
    sync = Sync.SHORT
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
    sync = Sync.SHORT
    velocity: b2Vec2

    @classmethod
    def Still(cls):
        return cls(velocity=b2Vec2((0, 0)))

    @classmethod
    def from_body(cls, body: b2Body):
        return cls(velocity=body.linearVelocity)


@dataclass
class Angle(Component):
    component_name = 'angle'
    sync = Sync.SHORT
    angle: float

    @classmethod
    def Straight(cls):
        return cls(angle=0)


@dataclass
class Box2DWorld(Component):
    component_name = 'box2d_world'
    sync = Sync.NO_SYNC
    world: b2World


@dataclass
class Box2DBody(Component):
    component_name = 'box2d_body'
    sync = Sync.LONG
    body: b2Body

    def __register_entity__(self, entity_id: str):
        self.body.userData = entity_id


@dataclass
class Collidable(Component):
    component_name = 'collidable'
    sync = Sync.NO_SYNC
    collides_with: Set[str] = field(default_factory=set)


@dataclass
class Ball(Component):
    component_name = 'ball'


@dataclass
class Player(Component):
    component_name = 'player'
    color: int


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


@dataclass
class Input(Component):
    component_name = 'input'
    sync = Sync.NO_SYNC
    move_left: bool
    move_right: bool
    jump: bool

    @classmethod
    def Nil(cls):
        return cls(move_left=False, move_right=False, jump=False)


COMPONENTS = list(filter(lambda cls: is_dataclass(cls) and issubclass(cls, Component), locals().values()))
SHORT_SYNC_COMPONENTS = list(filter(lambda cls: cls.sync == Sync.SHORT, COMPONENTS))
LONG_SYNC_COMPONENTS = list(filter(lambda cls: cls.sync != Sync.NO_SYNC, COMPONENTS))
