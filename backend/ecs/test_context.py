import pytest
from typing import TypedDict, Dict
from ecs.context import Context
from ecs.base_component import Component
from dataclasses import dataclass


@dataclass
class Foo(Component):
    component_name = 'foo'
    value: int


@dataclass
class Bar(Component):
    component_name = 'bar'
    value2: int


@dataclass
class SingleFoo(Component):
    component_name = 'singlefoo'
    value3: int


@dataclass
class NestedFoo(Component):
    component_name = 'nestedfoo'
    foo: Foo


MyRepository = TypedDict('MyRepository', {
    'foo': Dict[str, Foo],
    'bar': Dict[str, Bar],
    'singlefoo': Dict[str, SingleFoo]
}, total=False)


@pytest.fixture
def empty_repository():
    return MyRepository(foo={}, bar={}, singlefoo={})


class TestContext:
    def test_get_component(self, empty_repository):
        value = Foo(1)
        c = Context(repository=empty_repository)
        c.add('1', value)

        assert c.get_components('1', Foo) == (value,)

    def test_new_component(self, empty_repository):
        value = Foo(1)
        c = Context(repository=empty_repository)
        entity_id = c.new(value)

        assert entity_id == '0'
        assert c.get_components(entity_id, Foo) == (value,)

    def test_add_component_keeps_existing_data(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new(Foo(1))
        c.add(entity_id, Bar(2))

        assert c.get_components(entity_id, Foo, Bar) == (Foo(1), Bar(2))

    def test_add_singleton_component(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new_singleton(SingleFoo(1))

        assert entity_id == SingleFoo.component_name
        assert c.get_components(entity_id, SingleFoo) == (SingleFoo(1),)

    def test_get_singleton_component(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new_singleton(SingleFoo(1))

        assert entity_id == SingleFoo.component_name
        assert c.get_singleton(SingleFoo) == SingleFoo(1)
        assert c.get_singleton(SingleFoo, 'value3') == 1
        assert c.get_singleton(SingleFoo, 'nonexistent') is None
