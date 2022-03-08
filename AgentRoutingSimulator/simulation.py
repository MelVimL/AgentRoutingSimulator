from core.entities import EntityScheduler
from core.entities import Agent, Connection
from utils.common import Indentifiable
from network import Network
from utils.stats import Stats
from db.api import init_session as init_db
from db.api import SimulationAPI as db

class SimpleSimulation(Indentifiable):
    """

    """

    def __init__(self, name="NoName", config={}) -> None:
        init_db()
        self.name = name
        self.network = Network()
        self.simulation_key = db.create_simulation(str(self), config)
        self.stats = Stats(self.simulation_key)
        self.entity_scheduler = EntityScheduler()

    def update(self):
        self.entity_scheduler.update(self.get_time_step())
        self.increment_time_step()

    def get_time_step(self):
        return db.get_time_step(self.simulation_key)

    
    def increment_time_step(self):
        db.set_time_step(self.simulation_key, self.get_time_step()+1)

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
    
    def __str__(self) -> str:
        return "Simulation_{}({})".format(self.name, str(self.get_id())) 
