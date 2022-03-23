from core.behavior import Behavior
from core.entities import Agent, Connection
from queue import Queue


class AgentBehavior(Behavior):
    def get_agent(self) -> Agent:
        return self.behaving


class SimpleAgentUpdate(AgentBehavior):

    def __init__(self, update_function) -> None:
        self._update_function = update_function
        super().__init__()

    def update(self, time_step):
        return self._update_function(self.behaving, time_step)


class SimpleReceiver(AgentBehavior):

    def __init__(self) -> None:
        self.queue = Queue()

    def update(self, time_step: int) -> None:
        agent = self.get_agent()
        net = agent.get_network()
        for connection in net.get_connections(agent):
            if connection.has_message(agent):
                self.queue.put(connection.receive(agent))

    def has_message(self):
        return not self.queue.empty()


class SimpleSender(AgentBehavior):
    def __init__(self) -> None:
        self.queue = Queue()

    def update(self, time_step: int) -> None:
        while not self.queue.empty():
            self.send()

    def create_message(self, size):
        data = {"data" : "a"*(size)}
        self.queue.put(data)

    def send(self):
        agent = self.get_agent()
        net = agent.get_network()
        connections = net.get_connections(agent)
        data = self.queue.get()

        for connection in connections:
            connection.send(agent, data)
