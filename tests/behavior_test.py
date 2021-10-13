from tests.utils import EmptyEnity
from behavior.entities import LinearDecay, ExponetialDecay

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
        