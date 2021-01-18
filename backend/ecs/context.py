from typing import DefaultDict, Tuple, Set, TypeVar, Mapping, Generic, Type, Any, Union, Literal
from collections import defaultdict
from .base_component import Component

T = TypeVar('T', bound=Mapping)


class Context(Generic[T]):
    def __init__(self, repository: T):
        self.entities: DefaultDict[str, Set[str]] = defaultdict(set)
        self.repository = repository
        self._updated_entities: DefaultDict[str, Set[str]] = defaultdict(set)
        self._counter = 0

        self._init_entities(repository)

    def new(self, **components: Component) -> str:
        """Create new entity and assign random id"""
        pass

    def add(self, entity_id: str, *components: Component):
        """Create new entity with given id"""
        pass

    def new_singleton(self, component: Component) -> str:
        """Create new singleton entity"""
        pass

    def get_entites_with(self, *components: Type[Component]) -> Set[str]:
        """Return ids of entities with given components"""
        pass

    def get_updated_entities(self, reset=True) -> Set[str]:
        """Return ids of entities with any updated flag"""
        pass

    def get_updated_entities_with(self, *components: Type[Component], reset=True) -> Set[str]:
        """Return ids of entities with updated flag for any of given components"""
        pass

    def get_singleton(self, component: Type[Component], field: str = None):
        """Return singleton component dataclass"""
        pass

    def get_components(self, entity_id: str, *components: Type[Component]) -> Tuple[Component, ...]:
        """Return component dataclasses for given entity and classes"""
        pass

    def get_updated_components(self, entity_id: str, *components: Type[Component], reset=True) -> Tuple[Component, ...]:
        """Return only updated component dataclasses for given entity and classes"""
        pass

    def _new_id(self) -> str:
        id = str(self._counter)
        self._counter += 1
        return id

    def _init_entities(self, repository: T):
        for component, data in self.repository.items():
            self.entities[component] = set(data.keys())
