from __future__ import annotations
import numpy as np
from scipy.spatial import cKDTree

from core.entities import Agent
from utils.spatial import Quad, Position

class SpaceStorage:
    def put(self, agent: Agent):
        """
        Puts an Agent in space.
        """
        pass

    def remove(self, agent: Agent):
        """
        Removes an agent of space.
        """
        pass

    def in_distance(self, pos: Position, range: float):
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
       

    def put(self, agent: Agent):
        self._changed = True
        self.agents.append(agent)
        self.position_array.append(agent.get_position().to_tuple())

    def remove(self, agent):
        self._changed = True
        index = self.agents.index(agent)
        self.agents.pop(index)
        self.position_array.pop(index)
        

    def in_distance(self, agent: Agent, range: float):
        if self._changed or not self.tree:
            self.tree = cKDTree(data=np.array(self.position_array))
            self._changed = False
        
        res = self.tree.query_ball_point(agent.get_position().to_tuple(), range)
        return [self.index_to_agents.get(x) for x in res]

class Raster2D(SpaceStorage):
    """
    Next
    """
    def __init__(self) -> None:
        self.raster_map = {}

    def _raster_index_from(self, position: Position)-> tuple():
        pass
    
    def put(self, agent):
        pass

    def remove(self, agent):
        pass

    def in_distance(self, agent, range):
        pass

    
class Bucket(SpaceStorage):
    """
    Simplest way to store spatials. 
    Note: this is for setting the interface needed and also for validating faster versions.
    """
    def __init__(self) -> None:
       self.bucket: list() = []

    def put(self, agent: Agent):
        self.bucket.append(agent)

    def remove(self, agent: Agent):
        self.bucket.remove(agent)

    def in_distance(self, agent: Agent, range: float):
        result = []
        
        for other_agent in self.bucket:
            pos_a = agent.get_position()
            pos_b = other_agent.get_position()
            if pos_a.distance(pos_b) <= range:
                result.append(other_agent)

        return result
