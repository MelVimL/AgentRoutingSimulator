import pytest
import random as r
from core.entities import Agent, Connection
from examples.qrouting import QRoutingAgent, QMessage
from utils.spatial import Position
from network import Network
from simulation import SimpleSimulation
from factories import StatsFactory
import matplotlib.pyplot as plt


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


def test_estimation_value(sim):
    """
    """
    net = sim.get_network()
    agents = [x for x in net.get_agents()]
    for agent in agents:
        agent.add_behavior(QRoutingAgent(config={}))
    from_behavior = agents[0].get_behavior(QRoutingAgent)
    to_agent = agents[-1]

    assert from_behavior.neigbor_estimation(str(to_agent)) == 0.0


def test_neighbor_discovery(small_sim):
    r.seed(30)
    small_sim
    agent = r.choice(small_sim.get_agents())
    behavior = agent.get_behavior(QRoutingAgent)
    neighbors = behavior.get_neighbors()
    assert len(neighbors) == 2 and agent not in neighbors


def test_reply(small_sim):
    r.seed(40)
    agent = r.choice(small_sim.get_agents())
    behavior = agent.get_behavior(QRoutingAgent)
    neighbors = behavior.get_neighbors()
    neighbor = r.choice(neighbors)

    behavior.generate_message(neighbor)

    assert True


def test_estimation_value_big(big_sim):
    agents = big_sim.get_agents()
    r.seed(10)
    source = r.choice(agents).get_behavior(QRoutingAgent)
    destination = r.choice(agents)

    assert source.neigbor_estimation(str(destination)) == 0.0


def test_big_send(big_sim):
    agents = big_sim.get_agents()
    r.seed(20)
    source = r.choice(agents)
    destination = r.choice(agents)

    sender: QRoutingAgent = source.get_behavior(QRoutingAgent)
    message = sender.generate_message(destination=destination, size=2000)
    sender.send_message(message)

    for i in range(2000):
        big_sim.update()


def test_small_send(small_sim: SimpleSimulation):
    agents = small_sim.get_agents()
    small_sim.get_network().debug_plt()
    r.seed(20)
    
    for i in range(20000):
        source = r.choice(agents)
        destination = r.choice(agents)

        sender: QRoutingAgent = source.get_behavior(QRoutingAgent)
        message = sender.generate_message(destination=destination, size=2000)
        print(destination)
        print(source)
        sender.messages.append(message)
        small_sim.update()
        plot()


def plot():
    stats = StatsFactory.create()
    arival_times = [x for x in stats.get("message_arrival_time").values()]
    result = {}
    for x, y in arival_times:
        result.setdefault(x, []).append(y)

    xs = [x for x in result]
    ys = [sum(result[y])/len(result[y]) for y in xs]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xs, ys)
    plt.show()


def test_send_a_couple_of_messages(big_sim: SimpleSimulation):
    agents = big_sim.get_agents()
    big_sim.get_network().debug_plt()
    r.seed(20)
    messages: list[QMessage] = []

    for i in range(1000):
        for i in range(1):
            source = r.choice(agents)
            destination = r.choice(agents)

            sender: QRoutingAgent = source.get_behavior(QRoutingAgent)
            message = sender.generate_message(
                destination=destination, size=200)
            messages.append(message)

        for message in messages:
            sender.send_message(message)

        big_sim.update()

    stats = StatsFactory.create()

    arival_times = [x for x in stats.get("message_arrival_time").values()]
    result = {}
    for x, y in arival_times:
        result.setdefault(x, []).append(y)
    xs = [x for x in result]
    ys = [sum(result[y])/len(result[y]) for y in xs]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xs, ys)
    plt.show()


def test_medium_graph(medium_sim):
    agents = medium_sim.get_agents()
    medium_sim.get_network().debug_plt()
    r.seed(20)
    for i in range(20000):
        send_messages(100, agents)
        for i in range(4000):
            medium_sim.update()
        plot()


def send_messages(number, agents):
    messages: list[QMessage] = []
    for i in range(number):
        source = r.choice(agents)
        destination = r.choice(agents)
        sender: QRoutingAgent = source.get_behavior(QRoutingAgent)
        message = sender.generate_message(destination=destination, size=200)
        messages.append(message)

    for message in messages:
        sender.send_message(message)
