from tests.utils import PingBehavior, PongBehavior
from core import Agent
from behavior.agents import SimpleAgentUpdate
from utils.spatial import Position, Positions


ZERO = Positions.ZERO
DIAGONAL = Positions.DIAGONAL
UP = Positions.UP

def test_agent_id():
    a = Agent()
    
    assert a.get_id()

def test_spatial_function():
    a = Agent(ZERO).get_position()
    b = Agent(UP).get_position()

    assert a.distance(b) == 1.0 and a.distance(b) == b.distance(a)

def test_sending_agent():
    ether = {}
    ping = PingBehavior(ether)
    pong = PongBehavior(ether)
    
    a = Agent(Positions.ZERO)
    b = Agent(Positions.DIAGONAL)
    
    a.add_behavior(ping)
    b.add_behavior(pong)

    a.update(1)
    b.update(1)

    assert ether["mail"]

def testSimpleBehavior():
    a = Agent()
    def test_behavior(agent:Agent, time_step:int):
        env = agent.get_environment()
        api = agent.get_api()
        #net = agen
        env["Test"] = time_step
       

    a.add_behavior(SimpleAgentUpdate(test_behavior)) 

    for i in range(10):
        a.update(i)
    
    assert a.get_environment()["Test"] == 9



