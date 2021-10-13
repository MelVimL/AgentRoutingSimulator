from core.entities import Behavior


class SimpleAgentUpdate(Behavior):

    def __init__(self, update_function) -> None:
        self._update_function = update_function
        super().__init__()
    
    def update(self, time_step):

        return self._update_function(self.behaving, time_step)