from core.behavior import Behavior
from queue import Queue

class AgentBehavior(Behavior):
    def get_agent(self):
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
        for data in self.queue:
            self

    def create_message(self, size):
        data = bytes(size)
        self.queue.put(data)


class SimpleSender(AgentBehavior):

    def update(self, time_step: int) -> None:
        pass