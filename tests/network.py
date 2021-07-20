import pytest
from core import Network, Agent
from tests.utils import CountBehavior


def test_simplest_network():
    net = Network()

    assert net.graph.size == 0

def test_simple_network():
    net = Network()
    behavior = CountBehavior() # IMPORTANT: THIS USEAGE IS NOT RECOMMENDED. In optimal case it is adviced to use for each agent a own instance.
    
    for i in range(3):
        agent = Agent(x=i, y=i)
        agent.add(behavior)
        net.add_agent(agent=agent)
    
