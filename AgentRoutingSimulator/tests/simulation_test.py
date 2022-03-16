import pytest
from network import Network
from core.entities import Agent, Connection
from utils.spatial import Position
from simulation import SimpleSimulation
from utils.config import ConfigLoader

CONFIG_PATH_1 = "AgentRoutingSimulator/tests/data/test_sim_1.yaml"

@pytest.fixture
def config():
    ConfigLoader.set_path(CONFIG_PATH_1)
    return ConfigLoader.load()

@pytest.fixture
def net(config) -> Network:
    net = Network(config=config.get("Network"))

    a1 = Agent(position=Position(0, 0), config=config.get("Agent"))
    a2 = Agent(position=Position(0, 1), config=config.get("Agent"))
    a3 = Agent(position=Position(1, 0), config=config.get("Agent"))
    a4 = Agent(position=Position(1, 0), config=config.get("Agent"))

    net.connect(a1, a2, Connection(config=config.get("Connection")))
    net.connect(a2, a3, Connection(config=config.get("Connection")))
    net.connect(a4, a1, Connection(config=config.get("Connection")))
    net.connect(a2, a4, Connection(config=config.get("Connection")))

    return net


def test_simple_config(config: dict, net: Network):
    sim = SimpleSimulation(config=config.get("Simulation"))
    sim.get_entity_scheduler().add_all(net.get_agents())
    sim.get_entity_scheduler().add_all(net.get_all_connections())
    sim.add_network(net)

    assert all(x.config.get("test_param", False) for x in sim.get_entity_scheduler().get_all()) and net.config.get("net_test_param")


def test_simple_simulation(config, net):

    def connection_function(time_step: int, environment: dict, config: dict):
        pass

    def agent_function(time_step: int, environment: dict, config: dict):
        pass

    sim = SimpleSimulation()

    for i in range(20):
        sim.update()

    assert True
