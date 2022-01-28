from core.behavior import Behavior


class LinearDecay(Behavior):

    def __init__(self, start_value=100.0, decay_rate=.10) -> None:
        self.value = start_value
        self.decay_rate = decay_rate
        self.decay = self.value*self.decay_rate
        super().__init__()
    
    def update(self, time_step):
        self.value -= self.decay
        if self.value <= 0:
            self.value = 0
        
        return super().update(time_step)


class ExponetialDecay(Behavior):

    def __init__(self, start_value=100.0, decay_rate=.10) -> None:
        self.value = start_value
        self.decay_rate = decay_rate
        super().__init__()

    def update(self, time_step):
        self.value -= self.value * self.decay_rate
        if self.value <= 0:
            self.value = 0
        
        return super().update(time_step)
