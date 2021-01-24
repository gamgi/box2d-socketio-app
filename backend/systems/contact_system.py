from typing import Callable, Tuple
from ecs.base_system import System
from ecs.context import Context
from systems.physics_system import PhysicsSystem
from components import Box2DBody, Box2DWorld, Collidable
from Box2D import b2ContactListener, b2Contact


class ContactSystem(System):
    requires = [PhysicsSystem]

    def __init__(self, context: Context):
        self.context = context

    def on_game_init(self, room):  # type:ignore
        self._add_contact_listener()

    def _add_contact_listener(self):
        world = self._get_world()
        world.contactListener = EntityContactListener(
            begin_contact=self.begin_contact,
            end_contact=self.end_contact
        )

    def begin_contact(self, entity_a: str, entity_b: str):
        collides = {entity_a, entity_b}
        entity_ids = collides.intersection(self.context.get_entities_with(Box2DBody, Collidable))

        for entity_id in entity_ids:
            self.context.get_definitely(entity_id, Collidable).collides_with.update(collides - {entity_id})

    def end_contact(self, entity_a: str, entity_b: str):
        collides = {entity_a, entity_b}
        entity_ids = collides.intersection(self.context.get_entities_with(Box2DBody, Collidable))

        for entity_id in entity_ids:
            collidable = self.context.get_definitely(entity_id, Collidable)

            collidable.collides_with.discard(entity_a)
            collidable.collides_with.discard(entity_b)

    def _get_world(self):
        return self.context.singleton(Box2DWorld, field='world')


class EntityContactListener(b2ContactListener):
    def __init__(self, begin_contact: Callable = None, end_contact=None):
        b2ContactListener.__init__(self)
        self.begin_contact_callback = begin_contact
        self.end_contact_callback = end_contact

    def BeginContact(self, contact: b2Contact) -> None:
        if self.begin_contact_callback:
            entity_a, entity_b = self._get_entities(contact)
            if entity_a and entity_b:
                self.begin_contact_callback(entity_a, entity_b)

    def EndContact(self, contact: b2Contact) -> None:
        if self.end_contact_callback:
            entity_a, entity_b = self._get_entities(contact)
            if entity_a and entity_b:
                self.end_contact_callback(entity_a, entity_b)

    def PreSolve(self, contact, oldManifold) -> None:
        pass

    def PostSolve(self, contact, impulse) -> None:
        pass

    def _get_entities(self, contact: b2Contact) -> Tuple[str, str]:
        entity_a = contact.fixtureA.body.userData
        entity_b = contact.fixtureB.body.userData
        return entity_a, entity_b
