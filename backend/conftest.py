import pytest
from ecs.context import Context
from repository import repository_factory


@pytest.fixture
def empty_context():
    return Context(repository_factory())
