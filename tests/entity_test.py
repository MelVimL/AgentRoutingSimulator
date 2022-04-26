import pytest
from ars.core.entities import Entity
from ars.core.behavior import Behavior


class BehaviorBase(Behavior):
    def __init__(self, test):
        self.test = test


class BehaviorA(BehaviorBase):
    def update(self, tpf):
        self.test.append("A")


class BehaviorB(BehaviorBase):
    def update(self, tpf):
        self.test.append("B")


@pytest.fixture
def simple_entity() -> Entity:
    return Entity()


@pytest.fixture
def simple_behavior() -> Behavior:
    return Behavior()


def test_empty_entity(simple_entity: Entity):
    assert len(simple_entity) == 0


def test_add_behavior(simple_entity: Entity, simple_behavior: Behavior):

    simple_entity.add_behavior(simple_behavior)
    assert len(simple_entity) == 1


def test_delete_behavior(simple_entity: Entity, simple_behavior: Behavior):
    simple_entity.add_behavior(simple_behavior)
    simple_entity.remove_behavior(type(simple_behavior))
    assert len(simple_entity) == 0


def test_get_behavior(simple_entity: Entity, simple_behavior: Behavior):
    simple_entity.add_behavior(simple_behavior)

    assert simple_entity.get_behavior(Behavior) == simple_behavior


def test_priority(simple_entity: Entity):
    result = []
    simple_entity.add_behavior(BehaviorA(result), priority=0)
    simple_entity.add_behavior(BehaviorB(result), priority=1)

    simple_entity.update(1)

    assert result == ["A", "B"]
