class ConnectionAPI:
    pass


class NetAPI:
    #actions
    def connect(self, id):
        """
        """
        pass
    def disconnect(self, id):
        """
        """
        pass
    def send(self, to, mail):
        """
        """
        pass
    def receive(self):
        """
        """
        pass
    #info
    def connections(self):
        """
        This API call returns all connections of the caller.
        """
        pass

    def neigbors_in_range(self, range):
        pass

class Behavior:
    """
    This class is for adding certein behavior to classes that inherents the Behaving class.
    Basicly it adds an update function to an Entity(like Agent or Connection). This makes all entitys in the Simulation customizable.
    All Behavior have access to the environment of the enity the behavior is attached to. It is recommendet to implement the 
    """
    
    def update(self, time_step):
        pass
    
    def set_behaving(self, behaving):
        self.behaving = behaving


class Behaving:

    def __init__(self) -> None:
        self.behavior_map = {}

    def update(self, time_step):
        for key in sorted(self.behavior_map):
            self.behavior_map.get(key).update(time_step)

    def add_behavior(self, behavior, priority):
        behavior.set_behaving(self)
        self.behavior_map.setdefault(priority, []).append(behavior)
    
    def remove_behavior(self, behavior_type):
         for key in sorted(self.behavior_map):
            for i, behavior in self.behavior_map.get(key):
                if type(behavior) == behavior_type:
                    self.behavior_map.get(key).pop(i)


class Agent(Behaving):

    def __init__(self, x, y) -> None:
        super().__init__()
        self.id = ""
        self.x = x
        self.y = y
        self.api = NetAPI ()
        self.environment = {}

    def set_environment_limit(self, bytes):
        pass

    def set_computing_limit(self, zicles):
        pass
    

class Connection(Behaving):
    
    def __init__(self) -> None:
        super().__init__()
        self.environment = {}


class Network():
    
    def __init__(self, agents, connections) -> None:
        self.agents = agents
        self.connections = connections
        self.graph = next
    
    def add_agent(self, agent):
        pass
        #self.agents
    
    def add_connection(self, agent_a, agent_b, connection):
        pass
    #self
    
    def update(self, time_step):
        for connection in self.connections.values():
            connection.update(time_step)

        for agent in self.agents.values():
            agent.update(time_step)



class Simulation:
    
    def __init__(self) -> None:
        self.agents = {}
        self.connections = {}

    def update(self):
        pass
    
    def load(self, filename):
        pass

    def store(self):
        pass

    def store_replay(self):
        pass

    def add_behavior(self, behaving_entity, behavior_type):
        """
        This add to all Connections or Agents a certein behavior. For more informations see the Documentation on the Behavior class.
        """
        if behaving_entity == Agent:
            for agent in self.agents.values():
                agent.add(behavior_type())
        elif behaving_entity == Connection:
            for connection in self.connections.values():
                connection.add(behavior_type())
        else:
            raise AttributeError("Unknown Entity.")
