from typing import List, Optional, Tuple, Union
from dataclasses import dataclass, field
from py_ts_interfaces import Interface
from math import pi


@dataclass
class RoomMeta(Interface):
    id: str
    name: str
    players: List[str]
    max_players: int
    private: bool
    level: str


@dataclass
class GetRoomsDTO(Interface):
    rooms: List[RoomMeta]


@dataclass
class CreateRoomDTO(Interface):
    room: RoomMeta


@dataclass
class JoinRoomDTO(Interface):
    room: RoomMeta


@dataclass
class RectShapeData(Interface):
    x: Union[int, float]
    y: Union[int, float]
    width: int
    height: int
    fill: bool = field(default=False, init=False)
    form: str = field(default='rect', init=False)


@dataclass
class ArcShapeData(Interface):
    x: Union[int, float]
    y: Union[int, float]
    radius: int
    start_angle: float
    end_angle: float
    fill: bool = field(default=False, init=False)
    form: str = field(default='arc', init=False)

    @classmethod
    def Circle(cls, x: int, y: int, radius: int):
        return cls(x, y, radius, start_angle=0, end_angle=2 * pi)

    @classmethod
    def SemiCircle(cls, x: int, y: int, radius: int):
        return cls(x, y, radius, start_angle=pi, end_angle=2 * pi)

    @classmethod
    def from_b2Circlehape(cls, shape):
        return cls.Circle(x=shape.pos.x, y=shape.pos.y, radius=shape.radius)


@dataclass
class PolygonShapeData(Interface):
    x: Union[int, float]
    y: Union[int, float]
    vertices: List[Tuple[int, int]]
    fill: bool = field(default=False, init=False)
    form: str = field(default='polygon', init=False)

    @classmethod
    def from_b2PolygonShape(cls, shape):
        return cls(x=0, y=0, vertices=shape.vertices)


@dataclass
class ShortEntityData(Interface):
    id: str
    position: Optional[List[float]] = None
    velocity: Optional[List[float]] = None


@dataclass
class EntityData(Interface):
    id: str
    position: Optional[List[float]] = None
    velocity: Optional[List[float]] = None
    shape: Optional[Union[PolygonShapeData, ArcShapeData, RectShapeData]] = None


@dataclass
class ShortSyncDTO(Interface):
    updates: List[ShortEntityData]


@dataclass
class LongSyncDTO(Interface):
    updates: List[EntityData]


@dataclass
class ErrorDTO(Interface):
    error: bool
    code: int
    message: str
