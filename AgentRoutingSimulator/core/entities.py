from __future__ import annotations
from core.behaving import Behaving
from utils.common import Indentifiable
from utils.spatial import Position, Positions
from dataclasses import dataclass
from network import Network
from queue import Queue


class EntityScheduler:
    """
    """

    def __init__(self) -> None:
        """
        """
        self._entities: dict = {}

    def update(self, tpf: int) -> None:
        """
        """
        for priority in sorted(self._entities.keys()):
            for entity in self._entities.get(priority):
                entity.update(tpf)

    def add(self, entity: Entity, priority: int = 0):
        """
        """
        self._entities.setdefault(priority, []).append(entity)

    def remove(self, entity: Entity):
        """
        """
        for priority in sorted(self._entities.keys()):
            try:
                self._entities.get(priority).remove(entity)
            except ValueError as e:
                pass


class Entity(Indentifiable, Behaving):
    """
    Entity is the Base Class for agents and Connections.
    It provides an Identifier, The possibility to add Behavior and is Hashable.
    """

    def __repr__(self) -> str:
        return str(self.get_id())


class NetworkAccess:
    def set_network(self, network: Network) -> None:
        self.network = network

    def get_network(self) -> Network:
        return self.network


class Agent(Entity, NetworkAccess):
    """
    An Agent is an Entity that have spatial position and is a part of a Network.
    In addition add contrains to memory usage and computing cycles.
    """

    def __init__(self, position: Position = Positions.ZERO, network: Network = None, environment: dict = {}) -> None:
        super().__init__()
        self.position = position
        self.network = network
        self.environment = environment

    def get_position(self) -> Position:
        """
        Returns the positions of the Agent.
        """
        return self.position

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


class Connection(Entity, NetworkAccess):
    """
    A connection is an Enity which is 
    """
    IN = "IN"
    OUT = "OUT"

    @dataclass
    class Message:
        data: bytes
        size: int
        to_send: int

        def __init__(self, data) -> None:
            self.data = data
            self.size = len(data)
            self.to_send = self.size

        def transmit(self, bytes):
            if bytes >= self.to_send:
                bytes_left = bytes - self.to_send
                self.to_send = 0
                return bytes_left
            else:
                self.to_send -= bytes
                return 0

        def is_transmitted(self):
            return self.to_send == 0

    def __init__(self, agent_a, agent_b, network=None, environment={}) -> None:
        super().__init__()
        self.environment: dict = environment
        self.network: Network = network
        self.agents_to_messages = {agent_a: {Connection.IN: [],
                                             Connection.OUT: []},
                                   agent_b: {Connection.IN: [],
                                             Connection.OUT: []}}

    def send(self, agent, data):
        massages = self._get_messages(agent, Connection.IN)
        massages.insert(0, Connection.Message(data))

    def _get_messages(self, agent, mode):
        return self.agents_to_messages.get(agent).get(mode)

    def has_message(self, agent):
        messages = self._get_messages(agent, Connection.OUT)
        return bool(messages)

    def receive(self, agent):
        messages = self._get_messages(agent, Connection.OUT)
        return messages.pop().data

    def transfer_bytes(self, source, target, bytes):
        in_list = self._get_messages(source, Connection.IN)
        out_list = self._get_messages(target, Connection.OUT)

        while bytes != 0 and in_list:
            msg = in_list.pop()
            bytes = msg.transmit(bytes)
            if msg.is_transmitted():
                out_list.insert(0, msg)
            else:
                in_list.append(msg)

    def get_participants(self):
        return self.agents_to_messages.keys()
