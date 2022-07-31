from .core.entities import EntityScheduler
from .core.entities import Agent, Connection
from .utils.common import Indentifiable
from .network import Network
from .factories import StatsFactory
from .db.api import get_session as init_db
from .db.api import SimulationAPI as db


class SimpleSimulation(Indentifiable):
    """

    """

    def __init__(self, name="NoName", config={}) -> None:
        init_db()
        self.name = name
        self.network = Network()
        self.simulation_key = db.create_simulation(str(self), config)
        self.stats = StatsFactory.create(self.simulation_key)
        self.entity_scheduler = EntityScheduler()
        self.config = config

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

    def get_network(self) -> Network:
        return self.network

    def set_network(self, network: Network) -> None:
        self.network = network
        self.get_entity_scheduler().add_all(self.get_agents())
        #self.get_entity_scheduler().add_all(self.get_connections())

    def get_agents(self) -> list[Agent]:
        return self.get_network().get_agents()

    def get_connections(self) -> list[Connection]:
        return self.get_network().get_all_connections()

    def get_entity_scheduler(self) -> EntityScheduler:
        return self.entity_scheduler

    def __str__(self) -> str:
        return "Simulation_{}({})".format(self.name, str(self.get_id()))
