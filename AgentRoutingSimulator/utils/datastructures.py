from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.entities import Agent

import numpy as np
from scipy.spatial import cKDTree
from utils.spatial import Position


class SpaceStorage:
    def put(self, agent: Agent) -> None:
        """
        Puts an Agent in space.
        """
        pass

    def remove(self, agent: Agent) -> None:
        """
        Removes an agent of space.
        """
        pass

    def in_distance(self, pos: Position, range: float) -> list(Agent):
        """
        Returns all agents in range from position.
        """
        pass


class KDTree(SpaceStorage):
    """

    """

    def __init__(self) -> None:
        self.tree = None
        self.agents = []
        self.position_array = []
        self._changed = False

    def put(self, agent: Agent) -> None:
        self._changed = True
        self.agents.append(agent)
        self.position_array.append(agent.get_position().to_tuple())

    def remove(self, agent: Agent) -> None:
        self._changed = True
        index = self.agents.index(agent)
        self.agents.pop(index)
        self.position_array.pop(index)

    def in_distance(self, agent: Agent, range: float) -> list(Agent):
        if self._changed or not self.tree:
            self.tree = cKDTree(data=np.array(self.position_array))
            self._changed = False

        res = self.tree.query_ball_point(
            agent.get_position().to_tuple(), range)
        return [self.position_array[x] for x in res]


class Raster2D(SpaceStorage):
    """
    Next
    """

    def __init__(self) -> None:
        self.raster_map = {}

    def _raster_index_from(self, position: Position) -> tuple():
        pass

    def put(self, agent: Agent) -> None:
        pass

    def remove(self, agent: Agent) -> None:
        pass

    def in_distance(self, agent: Agent, range: Agent) -> list(Agent):
        pass


class Bucket(SpaceStorage):
    """
    Simplest way to store spatials. 
    Note: this is for setting the interface needed and also for validating faster versions.
    """

    def __init__(self) -> None:
        self.bucket: list() = []

    def put(self, agent: Agent) -> None:
        self.bucket.append(agent)

    def remove(self, agent: Agent) -> None:
        self.bucket.remove(agent)

    def in_distance(self, agent: Agent, range: float) -> list(Agent):
        result = []

        for other_agent in self.bucket:
            pos_a = agent.get_position()
            pos_b = other_agent.get_position()
            if pos_a.distance(pos_b) <= range:
                result.append(other_agent)

        return result
