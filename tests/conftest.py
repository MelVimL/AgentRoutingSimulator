import pytest
import networkx.generators.classic as nxg_classic
from examples.qrouting import QRoutingAgent
from ars.core.entities import Agent, Connection
from ars.utils.config import ConfigLoader
from ars.utils.spatial import Position
from ars.network import Network
from ars.simulation import SimpleSimulation
from ars.factories import AgentFactory, ConnectionFactory

CONFIG_PATH_1 = "./tests/data/test_sim_1.yaml"
CONFIG_PATH_2 = "./tests/data/test_sim_2.yaml"
CONFIG_PATH_3 = "./tests/data/test_sim_3.yaml"


def config_load(path=CONFIG_PATH_1):
    ConfigLoader.set_path(path)
    return ConfigLoader.load()


@pytest.fixture
def config():
    """
    """
    return config_load()


def hand_made_net(config) -> Network:
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
def sim(config):
    sim = SimpleSimulation(config=config.get("Simulation", {}))
    net = hand_made_net(config)
    sim.set_network(net)
    return sim


@pytest.fixture
def big_sim(config):
    sim = SimpleSimulation(config=config.get("Simulation", {}))
    net = big_q_binomial_tree(config)
    sim.set_network(net)
    return sim


def medium_sim_load(config):
    sim = SimpleSimulation(config=config.get("Simulation", {}))
    net = medium_q_dorogovtsev_goltsev_mendes_graph(config)
    sim.set_network(net)
    return sim


@pytest.fixture
def medium_sim(config):
    return medium_sim_load(config)


@pytest.fixture
def small_sim(config):
    sim = SimpleSimulation(config=config.get("Simulation", {}))
    net = small_q_binomial_tree(config)
    sim.set_network(net)
    return sim


def small_q_binomial_tree(config):
    net = Network()
    a_conf = config.get("Agent")
    c_conf = config.get("Connection")
    a_func = AgentFactory.create_mono_behavior(QRoutingAgent, a_conf)
    c_func = ConnectionFactory.generate_simple_wireless_func(c_conf)

    net.generate_graph(nxg_classic.binomial_tree(2), a_func, c_func)

    return net


def big_q_binomial_tree(config):
    net = Network()
    a_conf = config.get("Agent")
    c_conf = config.get("Connection")
    a_func = AgentFactory.create_mono_behavior(QRoutingAgent, a_conf)
    c_func = ConnectionFactory.generate_simple_wireless_func(c_conf)

    net.generate_graph(nxg_classic.binomial_tree(10), a_func, c_func)

    return net


def medium_q_dorogovtsev_goltsev_mendes_graph(config):
    net = Network()
    a_conf = config.get("Agent")
    c_conf = config.get("Connection")
    a_func = AgentFactory.create_mono_behavior(QRoutingAgent, a_conf)
    c_func = ConnectionFactory.generate_simple_wireless_func(c_conf)

    net.generate_graph(
        nxg_classic.dorogovtsev_goltsev_mendes_graph(3), a_func, c_func)

    return net
