from network import Network
from core.entities import Agent, Connection
from utils.spatial import Position
from simulation import SimpleSimulation


def test_simple_simulation():

    def connection_function(time_step: int, environment: dict, config: dict):
        pass

    def agent_function(time_step: int, environment: dict, config: dict):
        pass

    net = Network()
    a1 = Agent(position=Position(0,0))
    a2 = Agent(position=Position(0,0))
    a3 = Agent(position=Position(0,0))

    #net.connect(a1, a2, Connection)
    #net.connect(a3, a2, Connection)

    sim = SimpleSimulation()

    for i in range(20):
        sim.update()

    assert True