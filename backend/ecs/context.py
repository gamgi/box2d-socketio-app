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

    def new(self, *components: Component) -> str:
        """Create new entity and assign random id"""

        entity_id = self._new_id()
        self.add(entity_id, *components)
        return entity_id

    def add(self, entity_id: str, *components: Component) -> str:
        """Create new entity with given id"""

        self._add_entity_with_components(entity_id, components)
        self._update_components(entity_id, components)
        return entity_id

    def new_singleton(self, component: Component) -> str:
        """Create new singleton entity"""

        return self.add(component.component_name, component)

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

        value, = self.get(component.component_name, component)  # type:ignore
        if field:
            return getattr(value, field, None)
        return value

    def get(self, entity_id: str, *components: Type[Component]) -> Tuple[Component, ...]:
        """Return component dataclasses for given entity and classes"""

        return tuple(
            self.repository[component.component_name].get(entity_id, None) for component in components
        )

    def get_updated_components(self, entity_id: str, *components: Type[Component], reset=True) -> Tuple[Component, ...]:
        """Return only updated component dataclasses for given entity and classes"""

        pass

    def _new_id(self) -> str:
        entity_id = str(self._counter)
        self._counter += 1
        return entity_id

    def _init_entities(self, repository: T):
        for component, data in self.repository.items():
            self.entities[component] = set(data.keys())

    def _add_entity_with_components(self, entity_id: str, components: Tuple[Component, ...]):
        for component in components:
            self.entities[component.component_name].add(entity_id)

    def _update_components(self, entity_id: str, components: Tuple[Component, ...]):
        for component in components:
            self.repository[component.component_name][entity_id] = component
