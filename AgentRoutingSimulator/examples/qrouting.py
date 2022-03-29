from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid1
if TYPE_CHECKING:
    from core.entities import Agent
from dataclasses import dataclass
from behavior.agents import AgentBehavior


@dataclass
class QMessage():
    id: str
    destination: str
    sender: str
    _fake_payload: int

    def is_at_destination(self, agent):
        return str(agent) == self.destination


@dataclass
class QReply:
    sender: str
    s: float


@dataclass
class QUpdate():
    sender: str
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
        self.messages = []
        self.replys = []
        self.updates = []
        self._q_table: dict[str, float] = {}

        self.message_send_table: dict[str, list[QUpdate]] = {}

        super().__init__()

    def update(self, time_step: int) -> None:

        self.receive_all_messages()
        self.process_replies()
        self.process_messages()

        return super().update(time_step)

    def receive_all_messages(self):
        for message in self.receive_messages():
            if message.is_reply():
                self.replys.append(message)
            else:
                self.messages.append(message)

    def receive_messages(self):
        agent = self.get_agent()
        result = []
        for con in self.get_network().get_connections(agent):
            while con.has_message(agent):
                result.append(con.receive())
        return result

    def process_replies(self):
        for reply in sorted(self.replys):
            self.handle_reply(reply)

    def handle_reply(self, reply: QReply):
        self.update_
        self.update_table()

    def process_messages(self):
        if not self.messages:
            return
        message = self.get_message()
        agent = self.get_agent()
        self.send_reply(message)
        if message.is_at_destination(agent.get_id()):
            pass
        else:
            self.send_message(message)

    def send_reply(self, message):
        pass

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
        agent = self.get_agent()
        destination = message.destination
        neigbors = self.get_neighbors()
        next_hop = self.select_best_choice(neigbors, destination)

        q = len(self.messages)
        t = self.neigbor_estimation_request(destination, next_hop)
        old_q = self.quality_func(destination, next_hop)
        q_update = QUpdate(sender=str(agent),
                           destination=destination,
                           q=q, t=t, old_q=old_q)
        self.updates.append(q_update)

        self.send(message, next_hop)

    def update_table(self, update: QUpdate, reply: QReply):
        next_hop = update.sender
        s = reply.s
        q = update.q
        t = update.t
        old_q = update.old_q
        new_q = old_q + self.alpha * ((s + q + t) - old_q)

        self._q_table.get(update.destination).update({next_hop: new_q})

    def quality_func(self, destination, next_hop):
        destination_table = self._q_table.setdefault(destination, {})
        return destination_table.setdefault(next_hop, self.default_q)

    def neigbor_estimation_request(self, destination: str, next_hop: Agent):
        behavior = next_hop.get_behavior(QRoutingAgent)
        behavior.neigbor_estimation(destination, [self.get_agent()])

    def neigbor_estimation(self,
                           destination: str,
                           already_visited: list[str] = []) -> float:
        params = {"destination": destination,
                  "already_visited": list(already_visited)}
        this_agent = self.get_agent()
        params.get("already_visited").append(this_agent)
        if this_agent == destination:
            return 0.
        agents = self.without(self.get_neighbors(), already_visited)
        q_values = []
        for agent in agents:
            t = agent.get_behavior(QRoutingAgent).neigbor_estimation(**params)
            if t is not None:
                q = self.quality_func(destination, agent)
                q_values.append(q+t)
        if q_values:
            return min(q_values)
        else:
            return None

    def without(self, elements, excludes):
        result = []

        for e in elements:
            if e not in excludes:
                result.append(e)

        return result

    def generate_message(self, destination: Agent, size: int):
        sender_id = str(self.get_agent())
        destination_id = str(destination)
        return QMessage(id=str(uuid1()),
                        destination=destination_id,
                        sender=sender_id,
                        _fake_payload=size)

    def select_min(self, neigbors, destination):
        return min(neigbors, key=lambda x: self.quality_func(destination, x))

    def select_best_choice(self, neigbors, destination):
        return self.select_min(neigbors, destination)

    def get_neighbors(self):
        agent = self.get_agent()
        return [x for x in agent.get_network().get_neighbors(agent)]
