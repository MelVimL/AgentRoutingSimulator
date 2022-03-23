import pytest

from core.entities import Agent, Connection
from examples.qrouting import QRoutingAgent
from utils.config import ConfigLoader
from utils.spatial import Position
from network import Network

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


def test_estimation_value(net: Network):
    """
    """
    agents = [x for x in net.get_agents()]
    for agent in agents:
        agent.add_behavior(QRoutingAgent(config={}))
    from_agent = agents[0]
    to_agent = agents[-1]
    assert from_agent.get_behavior(QRoutingAgent).neigbor_estimation(to_agent.get_id(), 1., 1., [])


