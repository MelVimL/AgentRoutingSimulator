from core.entities import Connection, Agent
from tests.utils import EmptyEnity
from utils.spatial import Positions
from behavior.entities import LinearDecay, ExponetialDecay
from behavior.connections import  SimpleWireless
from behavior.agents import SimpleReceiver, SimpleSender
from network import Network


def test_linear_decay():
    e = EmptyEnity()
    d = LinearDecay()

    e.add_behavior(d)
    
    for i in range(10):
        e.update(i)

    assert d.value <= 0.1


def test_exponential_decay():
    e = EmptyEnity()
    d = ExponetialDecay(decay_rate=0.5)

    e.add_behavior(d)
    
    for i in range(3):
        e.update(i)

    assert d.value <= 12.5


def test_simple_Wireless():
    net = Network()
    a = Agent(Positions.UP)
    b = Agent(Positions.DOWN)
    
    r = SimpleReceiver()
    s = SimpleSender()
    
    a.add_behavior(s)
    b.add_behavior(r)

    c = Connection(a,b)
    w = SimpleWireless()
    
    c.add_behavior(w)

    net.connect(a,b,c)

    s.create_message(200)
    # Updates Entities
    a.update(0)
    c.update(0)
    b.update(0)
    assert r.has_message()
