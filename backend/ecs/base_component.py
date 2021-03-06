from typing import TYPE_CHECKING
from enum import Enum
from abc import ABC, abstractmethod


Sync = Enum('Sync', ['SHORT', 'LONG', 'NO_SYNC'])


if TYPE_CHECKING:
    class Component(ABC):
        component_name: str
        sync: Sync

        def __register_entity__(self, entity_id: str):
            pass
else:
    class Component(ABC):
        sync: Sync = Sync.NO_SYNC

        # attempts to ensure component_name is defined, but does cause some type trouble
        @property
        @classmethod
        @abstractmethod
        def component_name(cls) -> str:
            raise NotImplementedError()

        def __register_entity__(self, entity_id: str):
            pass


class NullComponent(Component):
    _component_name: str

    def __init__(self, component_name: str):
        self._component_name = component_name

    @property
    def component_name(self) -> str:  # type:ignore
        return self._component_name

    def __getattr__(self, key):
        return None

    def __bool__(self):
        return False
