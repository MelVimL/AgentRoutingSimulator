import pytest
from network import Network
from examples.qrouting import QRoutingAgent
from core.entities import Agent, Connection
from behavior.connections import SimpleWireless
from utils.spatial import Position
from simulation import SimpleSimulation
from utils.config import ConfigLoader
from factories import ConnectionFactory, AgentFactory

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
    a3 = Agent(position=Position(1, 1), config=config.get("Agent"))
    a4 = Agent(position=Position(1, 0), config=config.get("Agent"))

    net.connect(a1, a2, Connection(config=config.get("Connection")))
    net.connect(a2, a3, Connection(config=config.get("Connection")))
    net.connect(a3, a4, Connection(config=config.get("Connection")))
    net.connect(a4, a1, Connection(config=config.get("Connection")))
    net.connect(a2, a4, Connection(config=config.get("Connection")))

    return net


def test_simple_config(config: dict, net: Network):
    sim = SimpleSimulation(config=config.get("Simulation"))
    sim.set_network(net)
    entities = sim.get_entity_scheduler().get_all()
    params_set = [x.config.get("test_param", False) for x in entities]
    assert all(params_set) and net.config.get("net_test_param")


def test_simple_q_simulation(config, sim):
    net = sim.get_network()
    a_conf = config.get("Agent")
    c_conf = config.get("Connection")
    a_func = AgentFactory.create_mono_behavior(QRoutingAgent, a_conf)
    c_func = ConnectionFactory.create_mono_behavior(SimpleWireless, c_conf)
    net.generate_graph(net.graph, a_func, c_func)
    for i in range(20):
        sim.update()

    # net.debug_plt()

    assert True
