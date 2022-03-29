from core.entities import Agent, Connection
from network import Network
from utils.spatial import Position
from examples.qrouting import QRoutingAgent
from behavior.connections import SimpleWireless


class ConnectionFactory:

    @staticmethod
    def create_wireless_connection():
        connection = Connection()
        connection.add_behavior()
        connection.add_behavior()
        return connection

    @staticmethod
    def generate_simple_wireless_func(config):
        behavior_conf = config.get("Behavior")

        def func():
            c = Connection(config=config)
            c.add_behavior(SimpleWireless(behavior_conf.get("SimpleWireless")))
            return c

        return func


class AgentFactory:
    @staticmethod
    def generate_q_routing_agent_func(config):
        agent_config = config
        agent_behavior = config.get("Behavior")

        def func(position: Position):
            a = Agent(position=position, config=agent_config)
            a.add_behavior(QRoutingAgent(agent_behavior.get("QRoutingAgent")))
            return a

        return func


class NetworkFactory:

    @staticmethod
    def create_little_bottle_neck():
        """

        """
        net = Network()
        agents = [None]
        agents.append(Agent(Position(1., 2.)))
        agents.append(Agent(Position(2., 3.)))
        agents.append(Agent(Position(3., 2.)))
        agents.append(Agent(Position(2., 1.)))

        agents.append(Agent(Position(4., 2.)))
        agents.append(Agent(Position(5., 3.)))
        agents.append(Agent(Position(6., 2.)))
        agents.append(Agent(Position(5., 1.)))

        net.connect(agents[1], agents[2], Connection(agents[1], agents[2]))
        net.connect(agents[2], agents[3], Connection(agents[2], agents[3]))
        net.connect(agents[3], agents[4], Connection(agents[3], agents[4]))
        net.connect(agents[1], agents[4], Connection(agents[1], agents[4]))

        net.connect(agents[3], agents[5], Connection(agents[3], agents[5]))

        net.connect(agents[5], agents[6], Connection(agents[5], agents[6]))
        net.connect(agents[6], agents[7], Connection(agents[6], agents[7]))
        net.connect(agents[7], agents[8], Connection(agents[7], agents[8]))
        net.connect(agents[8], agents[5], Connection(agents[8], agents[5]))

        # net.debug_plt()
