from abc import ABC, abstractmethod


class Component(ABC):
    # attempts to ensure component_name is defined, but does cause some type trouble
    @property
    @classmethod
    @abstractmethod
    def component_name(cls) -> str:
        raise NotImplementedError()


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
