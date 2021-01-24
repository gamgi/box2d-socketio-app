import pytest
from unittest.mock import Mock, MagicMock
from systems.contact_system import ContactSystem, EntityContactListener
from components import Box2DWorld, Box2DBody, Collidable
from Box2D import b2Contact


@pytest.fixture
def world():
    return Box2DWorld(MagicMock(name='b2World'))


@pytest.fixture
def context(empty_context, world):
    empty_context.new_singleton(world)
    empty_context.upsert('body1', Box2DBody(Mock()), Collidable(set()))
    empty_context.upsert('body2', Box2DBody(Mock()), Collidable(set()))
    return empty_context


@pytest.fixture
def system(context):
    system = ContactSystem(context)
    return system


class TestContactSystem:
    def test_on_game_init_adds_contact_listener(self, system, world):
        system.on_game_init(None)

        assert isinstance(world.world.contactListener, EntityContactListener)

    def test_begin_contact_updates_collidable(self, system, context, world):
        system.on_game_init(None)
        contact: b2Contact = Mock()
        contact.fixtureA.body.userData = 'body1'
        contact.fixtureB.body.userData = 'body2'

        world.world.contactListener.BeginContact(contact)

        assert context.component('body1', Collidable).collides_with == {'body2'}
        assert context.component('body2', Collidable).collides_with == {'body1'}

    def test_end_contact_updates_collidable(self, system, context, world):
        system.on_game_init(None)
        context.component('body1', Collidable).collides_with.add('body2')
        context.component('body2', Collidable).collides_with.add('body1')

        contact: b2Contact = Mock()
        contact.fixtureA.body.userData = 'body1'
        contact.fixtureB.body.userData = 'body2'

        world.world.contactListener.EndContact(contact)

        assert context.component('body1', Collidable).collides_with == set()
        assert context.component('body2', Collidable).collides_with == set()
