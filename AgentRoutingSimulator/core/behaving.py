
class Behaving:

    def __init__(self) -> None:
        self.behavior_map = {}
        self.environment = {}

    def update(self, time_step):
        for key in sorted(self.behavior_map):
            for behavior in self.behavior_map.get(key):
                behavior.update(time_step)

    def add_behavior(self, behavior, priority=1):
        behavior.set_behaving(self)
        self.behavior_map.setdefault(priority, []).append(behavior)

    def remove_behavior(self, behavior_type):
        for key in sorted(self.behavior_map):
            for i, behavior in self.behavior_map.get(key):
                if type(behavior) == behavior_type:
                    self.behavior_map.get(key).pop(i)

    def get_environment(self):
        return self.environment
