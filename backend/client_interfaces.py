from typing import List, Optional
from dataclasses import dataclass
from py_ts_interfaces import Interface


@dataclass
class CreateRoomDTO(Interface):
    name: str
    private: bool


@dataclass
class JoinRoomDTO(Interface):
    room_id: str


@dataclass
class InputDTO(Interface):
    keys_down: List[str]
    keys_pressed: Optional[List[str]]
    keys_released: Optional[List[str]]
