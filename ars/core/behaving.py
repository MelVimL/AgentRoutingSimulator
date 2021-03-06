from __future__ import annotations
from typing import TYPE_CHECKING
from typing import TypeVar
if TYPE_CHECKING:
    from ..core.behavior import Behavior
    B = TypeVar('B', bound=Behavior)

from dataclasses import dataclass


def is_type(x, x_type):
    return type(x) == x_type


@dataclass(order=True)
class BehaviorContainer:
    priority: int
    behavior: Behavior


class Behaving:
    def __init__(self) -> None:
        self._behavior_containers = []
        self.environment = {}

    def update(self, time_step: int) -> None:
        for container in sorted(self._behavior_containers):
            container.behavior.update(time_step)

    def add_behavior(self, behavior: B, priority: int = 1) -> None:
        behavior.set_behaving(self)
        self._behavior_containers.append(BehaviorContainer(priority, behavior))

    def get_behavior(self, behavior_type: B) -> B:
        for container in self._behavior_containers:
            if type(container.behavior) == behavior_type:
                return container.behavior

    def remove_behavior(self, behavior_type: B) -> None:
        for i, container in enumerate(self._behavior_containers):
            if type(container.behavior) == behavior_type:
                self._behavior_containers.pop(i)
                return

    def get_environment(self):
        return self.environment

    def get_behaviors(self) -> list[B]:
        return [x.behavior for x in self._behavior_containers]

    def __len__(self):
        return len(self.get_behaviors())
