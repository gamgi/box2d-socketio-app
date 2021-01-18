import pytest
from typing import TypedDict, Dict
from ecs.context import Context
from ecs.base_component import Component, NullComponent
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
        c.upsert('1', value)

        assert c.get('1', Foo) == (value,)

    def test_get_nonexistent_component(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('1', Foo(1))

        value, = c.get('1', Bar)
        assert bool(value) is False
        assert isinstance(value, NullComponent)
        assert value.component_name == Bar.component_name

    def test_new_component(self, empty_repository):
        value = Foo(1)
        c = Context(repository=empty_repository)
        entity_id = c.new(value)

        assert entity_id == '0'
        assert c.get(entity_id, Foo) == (value,)

    def test_new_singleton_component(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new_singleton(SingleFoo(1))

        assert entity_id == SingleFoo.component_name
        assert c.get(entity_id, SingleFoo) == (SingleFoo(1),)

    def test_upsert_component_keeps_existing_data(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new(Foo(1))
        entity_id = c.upsert(entity_id, Bar(2))

        assert entity_id == '0'
        assert c.get(entity_id, Foo, Bar) == (Foo(1), Bar(2))

    def test_upsert_singleton(self, empty_repository):
        c = Context(repository=empty_repository)
        c.new_singleton(SingleFoo(1))
        entity_id = c.upsert_singleton(SingleFoo(2))

        assert entity_id == SingleFoo.component_name
        assert c.get_singleton(SingleFoo) == SingleFoo(2)

    def test_get_singleton_component(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new_singleton(SingleFoo(1))

        assert entity_id == SingleFoo.component_name
        assert c.get_singleton(SingleFoo) == SingleFoo(1)
        assert c.get_singleton(SingleFoo, 'value3') == 1
        assert c.get_singleton(SingleFoo, 'nonexistent') is None

    def test_get_nonexisten_singleton_component(self, empty_repository):
        c = Context(repository=empty_repository)
        c.new_singleton(SingleFoo(1))

        value = c.get_singleton(Foo)
        assert bool(value) is False
        assert isinstance(value, NullComponent)
        assert value.component_name == Foo.component_name

    def test_upsert_marks_entity_updated(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('1', Foo(1))

        assert c.get_updated_entities() == set('1')
        assert c.get_updated_entities() == set()

        c.upsert('1', Foo(2))

        assert c.get_updated_entities() == set('1')

    def test_upsert_singleton_marks_entity_updated(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('1', Foo(1))

        assert c.get_updated_entities() == set('1')
        assert c.get_updated_entities() == set()

        c.upsert('1', Foo(2))

        assert c.get_updated_entities() == set('1')
