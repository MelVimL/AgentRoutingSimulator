from core.entities import Agent, Connection
from network import SimpleNetwork


class SimpleSimulation:
    """
    
    """
    
    def __init__(self) -> None:
        self.agents = {}
        self.connections = {}
        self.network = SimpleNetwork()
        self.time_step = 0

    def update(self):
        
        for agent in self.agents:
            agent.update(self.time_step)
        
        for connection in self.connections:
            connection.update(self.time_step)

        self.time_step += 1
    
    def load(self, filename):
        pass

    def store(self):
        pass

    def store_replay(self):
        pass

    def add_behavior(self, behaving_entity, behavior_type):
        """
        This add to all Connections or Agents a certein behavior. For more informations see the Documentation on the Behavior class.
        """
        if behaving_entity == Agent:
            for agent in self.agents.values():
                agent.add(behavior_type())
        elif behaving_entity == Connection:
            for connection in self.connections.values():
                connection.add(behavior_type())
        else:
            raise AttributeError("Unknown Entity.")

