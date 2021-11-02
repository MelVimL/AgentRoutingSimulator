from __future__ import annotations
from core.entities import Agent
from utils.spatial import Quad, Position

class SpaceStorage:
    def put(self, agent: Agent):
        pass

    def remove(self, agent: Agent):
        pass

    def in_distance(self, agent: Agent, range: float):
        pass

class K2Tree:
    """
    
    """
    MAX_FLOAT = 200.
    MIN_FLOAT = 0.
    
    
    class Node:
        
        def __init__(self, quad: Quad) -> None:
            self.quad = quad
            self.data = None
            self.north = None 
            self.east = None
            self.south = None
            self.west = None
        
        def is_leaf(self):
            pass
            

    def __init__(self) -> None:
        self.root = K2Tree.Node(Quad())

    def put(self, agent):
        pass

    def remove(self, agent):
        pass

    def in_distance(self, agent, range):
        pass


class Raster2D:
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

    
class Bucket:
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
