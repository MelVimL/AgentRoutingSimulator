from ..core.entities import Connection
from ..core.behavior import Behavior
from ..utils.spatial import distance_of_agents
from math import pi, pow
from itertools import permutations
import logging

log = logging.getLogger("__main__")



class ConnectionBehavior(Behavior):
    """

    """

    def get_connection(self) -> Connection:
        return self.behaving


class Wireless(ConnectionBehavior):
    """

    """

    def __init__(self, config={}) -> None:
        self.config = config
        super().__init__()

    def update(self, time_step):
        connection: Connection = self.behaving
        participances = connection.get_participants()

        power = self.config.get("power", 100)
        damping = self.config.get("damping", 23)
        for a, b in permutations(permutations, 2):
            distance = distance_of_agents(a, b)
            signal_strength = power - \
                self.db_to_power(damping)/4*pi*pow(distance)
            bytes_per_timestep = 100
            bytes_per_participant = bytes_per_timestep//len(participances)


class SimpleWireless(ConnectionBehavior):
    """

    """

    def __init__(self, config={}) -> None:
        self.config = config
        self.max_range = self.config.get("max_range", 100.)
        self.max_bandwidth = self.config.get("max_bandwidth", 600.)
        self.time_step_length = self.config.get("time_per_step", 1.)
        super().__init__()

    def update(self, time_step):
        connection = self.get_connection()
        agents = connection.get_participants()
        agents_with_messages = [(a, b) for a, b in permutations(agents, 2)]
        bandwidth_per_agent = self.max_bandwidth/len(agents_with_messages)
        
        for a, b in agents_with_messages:
            distance = distance_of_agents(a, b)+0.000000000000000001 #ISSUE FIX WITH DESTINATION 0.0
            signal_strength = -(1/self.max_range)*distance**2+1
            throughput = round(bandwidth_per_agent *
                               signal_strength * self.time_step_length)
            log.info(f"{a} -> {b}")
            log.info(f"Distance: {distance}")
            log.info(f"throughput: {throughput}")
            connection.transfer_bytes(a, b, throughput)
        

class LinearConntection(ConnectionBehavior):
    """

    """

    _needed_config = ["cost_per_distance",
                      "max_range", "min_range", "max_bits_per_tick"]

    def __init__(self, config={}) -> None:
        self._valid_config(config)
        self.config = config
        super().__init__()

    def update(self, time_step):
        connection = self.get_connection()
        a, b = connection.get_agents()

        distance = distance_of_agents(a, b)
        bit_cost = self.config["cost_per_distance"]
        bit_loss = bit_cost * distance
        api = connection.get_api()

        for message in api.get_messages(a):
            api.send_to(b, message)

        for message in api.get_messages(b):
            api.send_to(a, message)

    def validate_config(self, config):
        for key in self._needed_config:
            if key not in config:
                raise AttributeError("The config needs '{}'".format(key))
