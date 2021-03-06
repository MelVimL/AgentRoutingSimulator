from ars.core.entities import Agent, Connection
from ars.utils.spatial import Positions, Position
from ars.network import Network
from itertools import permutations
import networkx.generators.classic as nxg_classics


def create_simple_network(size):
    network = Network()
    agents = (Agent(Position(i, i)) for i in range(size))

    for agent, other_agent in permutations(agents, 2):
        network.connect(agent, other_agent, connection=Connection())

    return network


def test_create_empty_network():
    net = Network()
    assert len(net.get_agents()) == 0


def test_connection():
    network = Network()
    agent_a = Agent(Positions.DOWN)
    agent_b = Agent(Positions.UP)
    c = Connection()
    # Here you can add Behaviors

    network.connect(agent_a=agent_a, agent_b=agent_b, connection=c)

    assert len(network.get_agents()) == 2 and len(
        network.get_all_connections()) == 1


def test_create_simple_network():
    a1 = Agent(Positions.DIAGONAL)
    a2 = Agent(Positions.DIAGONAL.scale(2.0))
    net = Network()

    net.add_agent(a1)
    net.add_agent(a2)
    connection = Connection(a1, a2)
    net.connect(agent_a=a1, agent_b=a2, connection=connection)

    assert len(net.get_agents()) == 2 and len(net.get_all_connections()) == 1


def test_get_all_connections():
    size = 3
    net = create_simple_network(size)
    # net.debug_plt()
    assert len(net.get_all_connections()) == 3


def test_get_connections():
    agent_a = Agent(Positions.ZERO)
    agent_b = Agent(Positions.DIAGONAL)
    c = Connection(agent_a, agent_b)
    net = Network()

    net.connect(agent_a, agent_b, c)

    assert c == net.get_connections(agent_a)[0]


def test_create_simple_generator_network():
    net = Network()

    def _test_gen_a(position: Position) -> Agent:
        a = Agent(position, config={})
        # a.add_behavior()
        return a

    def _test_gen_c() -> Connection:
        a = Connection(config={})
        # a.add_behavior()
        return a

    net.generate_graph(nxg_classics.binomial_tree(8), _test_gen_a, _test_gen_c)
    net.debug_plt()
