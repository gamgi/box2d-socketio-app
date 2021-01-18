from abc import ABC, abstractmethod


class Component(ABC):
    # attempts to ensure component_name is defined, but does cause some type trouble
    @property
    @classmethod
    @abstractmethod
    def component_name(cls) -> str:
        raise NotImplementedError()
