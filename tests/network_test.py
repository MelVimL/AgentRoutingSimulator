from core.entities import Agent, Connection
from utils.spatial import Positions
from network import Network

def test_create_empty_network():
    net = Network()
    assert len(net.get_agents()) == 0

def test_create_simple_network():
    a1 = Agent(Positions.DIAGONAL)
    a2 = Agent(Positions.DIAGONAL.scale(2.0))
    net = Network()

    net.add_agent(a1)
    net.add_agent(a2)
    connection = net.connect(agent_a=a1, agent_b=a2)

    assert len(net.get_agents()) == 2 and len(net.get_connections()) == 1

def test_create_simple_generator_network():
    pass

