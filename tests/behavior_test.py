from core.entities import Connection, Agent
from tests.utils import EmptyEnity
from behavior.entities import LinearDecay, ExponetialDecay
from behavior.connections import  SimpleWireless
from behavior.agents import SimpleReceiver, SimpleSender

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
    
    a = Agent()
    b = Agent()
    r = SimpleReceiver()
    s = SimpleSender()
    c = Connection(a,b)
    w = SimpleWireless()
    c.add_behavior(w)