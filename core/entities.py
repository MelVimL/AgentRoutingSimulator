from core.behaving import Behaving
from utils.common import Indentifiable
from utils.spatial import Position, Positions
from network import Network



class Entity(Indentifiable, Behaving):
    def __repr__(self) -> str:
        return str(self.get_id())


class EnitityProcessor:
    """
    This Class aggregates enities. 
    """
    def __init__(self) -> None:
        self.enities : list(Entity) = []

    def update(self, time_step: int) -> None:
        for entity in self.enities:
            entity.update(time_step)
    
    def add(self, entity: Entity) -> None:
        self.enities.append(entity)

    def remove(self, entity: Entity) -> None:
        self.enities.remove(entity)


class Agent(Entity):
    """
    An Agent is an Entity that have spatial Position and is a part of a Network.
    """

    def __init__(self, position: Position=Positions.ZERO, network: Network=None, environment: dict={}) -> None:
        super().__init__()
        self.position = position
        self.network = network
        self.environment = environment 

    def get_position(self) -> Position: 
        """
        Retruns the positions of the Agent.
        """
        return self.position
    
    def get_network(self) -> Network:
        """
        Returns the Network that the Agent is in.
        """
        return self.network

    def set_environment_limit(self, bytes: int) -> None:
        """
        Sets the limit of Bytes that can be stored in the environment.
        """
        pass

    def set_computing_limit(self, cicles: int) -> None:
        """
        Sets the Limit of Computing cycles.
        """
        pass
    

class Connection(Entity):
    
    def __init__(self, participants, network=None, environment={}) -> None:
        super().__init__()
        self.environment = environment
        self.network = network
        self.participants = participants

    def connect(self, id):
        pass

    def disconnect(self):
        pass

    def send(self, id, data):
        pass    
    
    def transfer_byte(self, agent1, agent2, data):
        pass

    def has_message(self):
        pass
    
    def receive(self, id):
        pass

    def get_participants(self):
        pass
  