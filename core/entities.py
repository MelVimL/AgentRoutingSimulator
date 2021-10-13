from abc import abstractmethod
from ..utils.common import Indentifiable
from ..utils.spatial import Positions

class Behavior:
    """
    This class is for adding certein behavior to classes that inherents the Behaving class.
    Basicly it adds an update function to an Entity(like Agent or Connection). This makes all entitys in the Simulation customizable.
    All Behavior have access to the environment of the enity the behavior is attached to. It is recommendet to implement the 
    """
    def __init__(self) -> None:
        self.enironment = {}
    
    @abstractmethod       
    def update(self, time_step):
        pass
    
    def set_behaving(self, behaving):
        self.behaving = behaving


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


class Entity(Indentifiable, Behaving):
    pass



class EnitityProcessor:
    """
    This Class aggregates enities. 
    """
    def __init__(self) -> None:
        self.enities = []

    def update(self, time_step):
        pass
    
    def add(self, entity):
        pass

    def remove(self, entity):
        pass


class Agent(Entity):

    def __init__(self, position=Positions.ZERO, network=None, environment={}) -> None:
        super().__init__()
        self.position = position
        self.network = network
        self.environment = environment
        

    def get_position(self):
        return self.position
    
    def get_api(self):
        return self.api
    
    def get_network(self):
        return self.network

    def set_environment_limit(self, bytes):
        pass

    def set_computing_limit(self, cicles):
        pass
    

class Connection(Entity):
    
    def __init__(self, participants, network=None, environment={}) -> None:
        super().__init__()
        self.environment = environment
        self.network = network
        self.participants = participants
        

    def connect(self, id):
        self.environment.setdefault("data", {}).update({id: {
            #
        }})

    def _get_data(self, id):
        return self.environment["data"][id]

    def send(self, id, data):
        in_queue = self.get_out_queue(id)
        #return out.pop().data()
        
    
    def receive(self, id, data):
        out = self.get_out_queue(id)
        return out.pop().data()

    def get_in_queue():
        pass

    def get_out_queue():
        pass

    def get_participants(self):
        return self.participants
