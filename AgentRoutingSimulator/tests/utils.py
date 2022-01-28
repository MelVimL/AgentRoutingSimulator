from core.entities import Agent
from core.behaving import Behaving
from core.behavior import Behavior

class PingBehavior(Behavior):
    def __init__(self, ether) -> None:
        self.ether = ether
        super().__init__()


    def update(self, time_step):
        if "mail" not in self.ether:
            self.ether["mail"] = False
        return super().update(time_step)

class PongBehavior(Behavior):
    def __init__(self, ether) -> None:
        self.ether = ether
        super().__init__()


    def update(self, time_step):
        if "mail" in self.ether:
            self.ether["mail"] = True
        return super().update(time_step)

class SenderAndReceiverAgent(Agent):

    def __init__(self, x, y, ) -> None:
        super().__init__(x=x, y=y)
    

class EmptyEnity(Behaving):
    pass

