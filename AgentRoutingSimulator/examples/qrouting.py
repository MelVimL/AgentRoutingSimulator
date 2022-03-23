from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.entities import Agent

from dataclasses import dataclass
from itertools import permutations
from queue import Queue
from utils.spatial import distance_of_agents
from behavior.agents import AgentBehavior
from behavior.connections import ConnectionBehavior


@dataclass
class QMessage():
    id: str
    type: str
    destination: str
    sender: str
    _fake_payload: int

    def is_reply(self):
        return self.type == "REPLY"

    def is_at_destination():
        pass


@dataclass
class QUpdate():
    destination: str
    q: float
    t: float
    old_q: float


class QRoutingAgent(AgentBehavior):

    def __init__(self, config) -> None:
        self.alpha = config.get("alpha", 0.)
        self.beta = config.get("beta", 0.5)
        self.delta = config.get("delta", 1.)
        self.default_q = config.get("default_q_value", 0.)
        self.message_queue = Queue()
        self._q_table: dict[str, float] = {}
        self.message_send_table: dict[str, list[QUpdate]] = {}

        super().__init__()

    def update(self, time_step: int) -> None:
        agent = self.get_agent()
        self.receive_messages()

        if self.has_messages():
            message = self.get_message()
            if message.is_at_destination(agent.get_id()):
                pass
            elif message.is_reply():
                self.update_table(message)
            else:
                self.send_message(message)

        return super().update(time_step)

    def get_network(self):
        agent = self.get_agent()
        return agent.get_network()

    def receive_messages(self):
        agent = self.get_agent()
        for con in self.get_network().get_connections(agent):
            while con.has_message(agent):
                self.message_queue.put(con.receive())

    def has_messages(self):
        agent = self.get_agent()

        for con in self.get_network().get_connections(agent):
            if con.has_message(agent):
                return True

        return False

    def send_message(self, message: QMessage):
        destination = message.get_destination()
        neigbors = self.get_neigbors()
        next_hop = self.select_best_choice(neigbors, destination)

        q = len(self.message_queue)
        t = self.neigbor_estimation(destination, next_hop)
        old_q = self.quality_func(destination, next_hop)

        self._t_table.update({self.message.id: QUpdate(q=q, t=t, old_q=old_q)})

        self.send(message, next_hop)

    def update_table(self, message: QMessage):

        next_hop = message.sender
        q_update = self._t_table.get(next_hop)
        s = message.get_transmission_time()
        q = q_update.q
        t = q_update.t
        old_q = q_update.old_q
        new_q = old_q + self.alpha * ((s + q + t) - old_q)

        self._q_table.get(message.destination).update({next_hop: new_q})

    def quality_func(self, destination, next_hop):
        destination_table = self._q_table.setdefault(destination, {})
        return destination_table.setdefault(next_hop, self.default_q)

    def neigbor_estimation_request(self, destination: str, next_hop: Agent):
        behavior = next_hop.get_behavior(QRoutingAgent())
        behavior.neigbor_estimation(destination, self.beta, self.delta, [
                                    self.get_agent().get_id()])

    def neigbor_estimation(self, destination: str, beta: float, delta: float,
                           already_visited: list[str]):
        agent_id = self.get_agent().get_id()

        if agent_id in already_visited:
            return None
        if agent_id == destination:
            return 0.

        already_visited = list(already_visited)
        already_visited.append(agent_id)
        q_results = list()
        for agent in self.get_neigbors():
            behavior = agent.get_behavior(QRoutingAgent)
            value = behavior.neigbor_estimation(
                destination, beta, delta, already_visited)
            q_results.append((agent, value))
        agent, estimated_value = min(q_results, key=lambda x: x[0])
        return self.quality_func(destination, agent) + estimated_value

    def select_min(self, neigbors, destination):
        return min(neigbors, lambda x: self.quality_func(destination, x))

    def select_best_choice(self, neigbors, destination):
        return self.select_min(neigbors, destination)

    def get_neigbors(self):
        agent = self.get_agent()
        return [agent.get_network().get_graph().neigbors(agent)]


class QRoutingConnection(ConnectionBehavior):
    def __init__(self, config={}) -> None:
        self.config = config
        self.max_range = self.config.get("max_range", 100.)
        self.max_bandwidth = self.config.get("max_bandwidth", 600.)
        self.time_step_length = self.config.get("time_per_step", 1.)
        super().__init__()

    def update(self, time_step):
        connection = self.get_connection()
        agents = connection.get_participants()
        agents_with_messages = [(a, b) for a, b in permutations(agents, 2)]
        bandwidth_per_agent = self.max_bandwidth/len(agents_with_messages)

        for a, b in agents_with_messages:
            connection.view_message()
            distance = distance_of_agents(a, b)
            signal_strength = -(1/self.max_range)*distance**2+1
            throughput = round(bandwidth_per_agent *
                               signal_strength * self.time_step_length)

            connection.transfer_bytes(a, b, throughput)
