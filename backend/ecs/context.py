from typing import DefaultDict, Tuple, Set, TypeVar, Mapping, Generic, Type, Union
from collections import defaultdict
from .base_component import Component, NullComponent

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
        self.upsert(entity_id, *components)
        return entity_id

    def new_singleton(self, component: Component) -> str:
        """Create new singleton entity"""

        return self.upsert(component.component_name, component)

    def upsert(self, entity_id: str, *components: Component) -> str:
        """Create or update entity with given id"""

        self._add_entity_with_components(entity_id, components)
        self._update_components(entity_id, components)
        self.mark_entity_updated(entity_id, *components)
        return entity_id

    def upsert_singleton(self, component: Component) -> str:
        """Create or update singleton entity with given id"""

        return self.upsert(component.component_name, component)

    def get_entites_with(self, *components: Type[Component]) -> Set[str]:
        """Return ids of entities with given components"""

        pass

    def get_updated_entities(self, reset=True) -> Set[str]:
        """Return ids of entities with any updated flag"""

        entity_ids_list = self._updated_entities.values()
        if entity_ids_list:
            updated = set.union(*entity_ids_list)
        else:
            return set()

        if reset:
            self._updated_entities.clear()

        return updated

    def get_updated_entities_with(self, *components: Type[Component], reset=True) -> Set[str]:
        """Return ids of entities with updated flag for any of given components"""

        updated = set.union([self._updated_entities[component.component_name]  # type:ignore
                             for component in components])
        if reset:
            for component in components:
                self._updated_entities[component.component_name] -= updated  # type:ignore
        return updated

    def get_singleton(self, component: Type[Component], field: str = None):
        """Return singleton component dataclass"""

        value, = self.get(component.component_name, component)  # type:ignore
        if field:
            return getattr(value, field, None)
        return value

    def get(self, entity_id: str, *components: Type[Component]) -> Tuple[Component, ...]:
        """Return component dataclasses for given entity and classes"""

        return tuple(
            self.repository[component.component_name].get(
                entity_id,
                NullComponent(component.component_name)  # type:ignore
            )
            for component in components)

    def get_updated_components(self, entity_id: str, *components: Type[Component], reset=True) -> Tuple[Component, ...]:
        """Return only updated component dataclasses for given entity and classes"""

        pass

    def mark_entity_updated(self, entity_id: str, *components: Union[Type[Component], Component]):
        """Marks entity updated to be retrieved for get_updated_nnn"""

        for component in components:
            self._updated_entities[component.component_name].add(entity_id)  # type:ignore

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
