from __future__ import annotations
from typing import TYPE_CHECKING
from .ars.factories import StatsFactory
from uuid import uuid1
if TYPE_CHECKING:
    from ars.core.entities import Agent
from dataclasses import dataclass, asdict
from behavior.agents import AgentBehavior
import networkx as nx
import random as r


@dataclass
class QMessage():
    id: str
    destination: str
    sender: str
    trasmission_time: float
    _fake_payload: int

    def is_at_destination(self, agent):
        return str(agent) == self.destination

    def get_size(self):
        return self._fake_payload + 12


class QRoutingAgent(AgentBehavior):

    def __init__(self, config) -> None:
        self.__init__learn(config)
        self.__init__communicator(config)
        self.stats = StatsFactory.create()
        super().__init__()

    def __init__learn(self, config):
        self.ALPHA = config.get("alpha", 0.)
        self.BETA = config.get("beta", 0.5)
        self.DELTA = config.get("delta", 1.)
        self.DEFAULT_Q = config.get("default_q_value", 0.)
        self._q_table: dict[str, float] = {}

    def __init__communicator(self, config):
        self.DISTANCE_SCALE = config.get("distance_scale", 1.)
        self.messages = []
        self.neighbors = []

    def update(self, time_step: int) -> None:
        self.update_wait_time()
        self.process_messages()
        self.receive_all_messages()

        return super().update(time_step)

    def receive_all_messages(self):
        for message in self.receive_messages():
            self.messages.append(message)

    def receive_messages(self):
        agent = self.get_agent()
        result = []
        for con in self.get_network().get_connections(agent):
            while con.has_message(agent):
                message = self._receive(con, agent)
                result.append(message)
        if result:
            print("")
        return result

    def _receive(self, connection, agent):
        d = connection.receive(agent)
        return QMessage(**d)

    def process_messages(self):
        if not self.messages:
            return
        message = self.get_message()
        agent = self.get_agent()
        if message.is_at_destination(agent):
            print(f"Hallo!: {message.trasmission_time}")
            self.stats.get("message_arrival_time")\
                .gather(message.trasmission_time)
        else:
            self.send_message(message)

    def update_wait_time(self):
        for message in self.messages:
            message.trasmission_time += 1.0

    def get_message(self):
        message = self.messages.pop()
        return message

    def get_network(self):
        agent = self.get_agent()
        return agent.get_network()

    def has_messages(self):
        agent = self.get_agent()

        for con in self.get_network().get_connections(agent):
            if con.has_message(agent):
                return True

        return False

    def send_message(self, message: QMessage):
        destination = message.destination
        next_hop = self.select_best_choice(destination).get_agent()

        q = len(self.messages)
        t = self.neigbor_estimation_request(destination, next_hop)
        old_q = self.quality_func(destination, next_hop)
        s = self._send_message(message, next_hop)

        self.update_table(s=s, q=q, t=t, old_q=old_q, destination=destination,
                          choice=next_hop)

    def _send_message(self, message: QMessage, next_hop: Agent):
        agent = self.get_agent()
        net = agent.get_network()
        connection = net.get_connection(agent, next_hop)
        connection.send(agent, asdict(message))
        s = self._distance_func(agent, next_hop)*message.get_size()
        message.trasmission_time += s
        return s

    def _distance_func(self, a, b):
        return a.get_position().distance(b.get_position())

    def update_table(self, s, q, t, old_q, destination, choice):

        new_q = old_q + self.ALPHA * ((s + q + t) - old_q)
        self._q_table.get(destination).update({choice: new_q})

    def quality_func(self, destination, next_hop):
        destination_table = self._q_table.setdefault(destination, {})
        return destination_table.setdefault(next_hop, self.DEFAULT_Q)

    def neigbor_estimation_request(self, destination: str, next_hop: Agent):
        #behavior = next_hop.get_behavior(QRoutingAgent)
        # behavior.dijkstra_estimation(destination)
        return self.T(destination)

    def get_flag():
        pass

    def set_flag():
        pass

    def dijkstra_estimation(self, destination):
        def weight_func(u, v, d):
            u_behavior = u.get_behavior(QRoutingAgent)
            v_behavior = v.get_behavior(QRoutingAgent)

            if u_behavior.get_mark() is None:
                u_behavior.set_mark(1)
            new_mark = u_behavior.get_mark() + 1
            v_behavior.set_mark(new_mark)

            weight = u_behavior.quality_func(destination, v)

            return weight * pow(self.DELTA, u_behavior.get_mark())

        destination = self.get_network().get_agent_by_name(destination)
        graph = self.get_network().get_graph()
        path = nx.shortest_path(graph, self.get_agent(),
                                destination, weight_func, 'dijkstra')
        result = 0.0
        elements = [x for x in enumerate(zip(path, path[1:]))]
        for i, (u, v) in reversed(elements):
            u_behavior = u.get_behavior(QRoutingAgent)
            result += u_behavior.quality_func(destination, v)
            if i != 0:
                result *= self.DELTA

        return result

    def T(self, destination, i=10):
        delta = self.DELTA
        next_hop = self.select_best_choice(destination)
        Q = self.quality_func(destination, next_hop.get_agent())
        if str(self.get_agent()) == destination:
            return 0.0
        if i < 0:
            return Q

        T = next_hop.T(destination, i-1)
        return (1 - delta) * Q + delta * T

    def without(self, elements, excludes):
        result = []

        for e in elements:
            if e not in excludes:
                result.append(e)

        return result

    def generate_message(self, destination: Agent, size: int = 2):
        sender_id = str(self.get_agent())
        destination_id = str(destination)
        return QMessage(id=str(uuid1()),
                        destination=destination_id,
                        sender=sender_id,
                        trasmission_time=0.,
                        _fake_payload=size)

    def select_min(self, destination):
        ns = [n.get_behavior(QRoutingAgent) for n in self.get_neighbors()]
        return min(ns, key=lambda x: self.quality_func(destination, x))

    def select_best_choice(self, destination):
        return self.select_min(destination)

    def best_choice_quality(self, destination):
        next_hop = self.select_best_choice.get_agent()
        return self.quality_func(destination, next_hop)

    def get_neighbors(self):
        return self.get_network().get_neighbors(self.get_agent())
