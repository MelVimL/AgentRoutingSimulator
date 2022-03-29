import pytest
import networkx.generators.classic as nxg_classic
from core.entities import Agent, Connection
from utils.config import ConfigLoader
from utils.spatial import Position
from network import Network
from factories import AgentFactory, ConnectionFactory

CONFIG_PATH_1 = "AgentRoutingSimulator/tests/data/test_sim_1.yaml"


@pytest.fixture
def config():
    """
    """
    ConfigLoader.set_path(CONFIG_PATH_1)
    return ConfigLoader.load()


@pytest.fixture
def net(config) -> Network:
    """
    """
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


@pytest.fixture
def big_q_binomial_tree(config):
    net = Network()
    a_conf = config.get("Agent")
    c_conf = config.get("Connection")
    a_func = AgentFactory.generate_q_routing_agent_func(a_conf)
    c_func = ConnectionFactory.generate_simple_wireless_func(c_conf)

    net.generate_graph(nxg_classic.binomial_tree(10), a_func, c_func)

    return net
