import pytest

from core.entities import Agent, Connection
from examples.qrouting import QRoutingAgent

from utils.spatial import Position
from network import Network


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
    from_behavior = agents[0].get_behavior(QRoutingAgent)
    to_agent = agents[-1]

    assert from_behavior.neigbor_estimation(to_agent, []) == 0.0

