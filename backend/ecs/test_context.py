from typing import TypedDict, Dict
import pytest
from unittest.mock import MagicMock, ANY
from operator import itemgetter
from ecs.context import Context
from ecs.base_component import Component, NullComponent
from ecs.exc import UnknownComponentError
from dataclasses import dataclass


@dataclass
class Foo(Component):
    component_name = 'foo'
    value: int

    def __register_entity__(self, entity_id: str):
        self.secret = entity_id


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


@dataclass
class Fake(Component):
    component_name = 'fake'


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

    def test_get_nonexistent_component_class(self, empty_repository):
        c = Context(repository=empty_repository)

        with pytest.raises(UnknownComponentError):
            c.get('1', Fake)

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

    def test_get_maybe(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new(Foo(1))

        assert c.get_maybe(entity_id, Foo) == Foo(1)
        value = c.get_maybe(entity_id, Bar)
        assert isinstance(value, NullComponent)
        assert value.something is None

    def test_get_definitely(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new(Foo(1))

        assert c.get_definitely(entity_id, Foo) == Foo(1)
        assert c.get_definitely(entity_id, Bar) is None

    def test_all(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('0', Foo(1))
        c.upsert('1', Bar(2))
        c.upsert('2', Foo(3), Bar(4))

        unsorted_data = c.all(Foo, optional_components=[Bar])
        data = sorted(unsorted_data, key=itemgetter(0))
        assert data[0] == ('0', Foo(1), ANY)
        assert data[1] == ('2', Foo(3), Bar(4))
        assert isinstance(data[0][2], NullComponent)

    def test_all_dict(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('0', Foo(1))
        c.upsert('1', Bar(2))
        c.upsert('2', Foo(3), Bar(4))

        data = c.all_dict(Foo, optional_components=[Bar])
        assert data == {
            '0': (Foo(1), ANY),
            '2': (Foo(3), Bar(4)),
        }

    def test_upsert_component_keeps_existing_data(self, empty_repository):
        c = Context(repository=empty_repository)
        entity_id = c.new(Foo(1))
        entity_id = c.upsert(entity_id, Bar(2))

        assert entity_id == '0'
        assert c.get(entity_id, Foo, Bar) == (Foo(1), Bar(2))

    def test_upsert_nonexistent_component_class(self, empty_repository):
        c = Context(repository=empty_repository)

        with pytest.raises(UnknownComponentError):
            c.upsert('1', Fake)  # type: ignore

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

        assert c.get_all_updated_entities() == set('1')
        assert c.get_all_updated_entities() == set()

        c.upsert('1', Foo(2))

        assert c.get_all_updated_entities() == set('1')

    def test_upsert_calls_register_entity(self, empty_repository):
        c = Context(repository=empty_repository)
        callback = MagicMock()
        c.upsert('my_id', MagicMock(component_name='foo', __register_entity__=callback))

        callback.assert_called_with('my_id')

    def test_upsert_singleton_marks_entity_updated(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('1', Foo(1))

        assert c.get_all_updated_entities() == set('1')
        assert c.get_all_updated_entities() == set()

        c.upsert('1', Foo(2))

        assert c.get_all_updated_entities() == set('1')

    def test_get_updated_entities(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('1', Foo(1))
        c.upsert('2', Bar(2))
        c.get_all_updated_entities(reset=True)

        assert c.get_updated_entities_for(Bar) == set()

        c.upsert('1', Foo(2))
        c.upsert('2', Bar(3))

        assert c.get_updated_entities_for(Bar) == set('2')
        assert c.get_all_updated_entities(reset=False) == set('1')
        assert c.get_updated_entities_for(Foo) == set('1')
        assert c.get_all_updated_entities() == set()
        assert c.get_updated_entities_for(Foo) == set()

    def test_get_updated_entities_for_nonexistent(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('1', Foo(1))

        assert c.get_updated_entities_for(Bar) == set()

    def test_get_updated_nonexistent_class(self, empty_repository):
        c = Context(repository=empty_repository)

        assert c.get_updated_entities_for(Fake) == set()

    def test_get_updated(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('1', Foo(1))
        c.upsert('2', Bar(2))
        c.get_all_updated_entities(reset=True)

        a = c.get_updated('2', Foo, Bar)
        assert a == (None, None)

        c.upsert('1', Foo(2))
        c.upsert('2', Bar(3))

        assert c.get_updated('2', Foo, Bar) == (None, Bar(3))
        assert c.get_updated('2', Foo, Bar) == (None, None)
        assert c.get_updated('1', Foo, Bar) == (Foo(2), None)

    def test_get_entities_with(self, empty_repository):
        c = Context(repository=empty_repository)
        c.upsert('1', Foo(1))
        c.upsert('2', Bar(2))
        c.upsert('3', Foo(3), Bar(4))

        assert c.get_entities_with(Foo) == {'1', '3'}
        assert c.get_entities_with(Bar) == {'2', '3'}

    def test_get_entities_with_nonexistent_class(self, empty_repository):
        c = Context(repository=empty_repository)
        assert c.get_entities_with(Fake) == set()
