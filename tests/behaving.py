from core import Behavior


class CountBehavior(Behavior):

    def __init__(self) -> None:
        super().__init__()
        self.count = 0
    
    def update(self, time_step):
        self.count += 1
