from core import Behavior, Connection
from math import pi, pow
from itertools import permutations


def distance_of_agents(a, b):
    return a.get_position().distance(b.get_position())

class Wireless(Behavior):

    def __init__(self, config) -> None:
        self.config = config
        super().__init__()
    
    def update(self, time_step):
        connection: Connection = self.behaving
        participances = connection.get_participants()
        
        power = self.config.get("power", 100)
        damping = self.config.get("damping", 23)
        for a, b in permutations(permutations, 2):
            distance = distance_of_agents(a, b)
            signal_strength = power-self.db_to_power(damping)/4*pi*pow(distance)
            bytes_per_timestep = 100
            bytes_per_participant = bytes_per_timestep//len(participances)
      
            



        
        


        

class LinearConntection(Behavior):
    _needed_config = ["cost_per_distance", "max_range", "min_range", "max_bits_per_tick"]

    
    def __init__(self, config) -> None:
        self._valid_config(config)
        self.config = config
        super().__init__()
    
    def update(self, time_step):
        connection = self.behaving
        a, b = connection.get_agents()

        distance = distance_of_agents(a, b)
        bit_cost = self.config["cost_per_distance"]
        bit_loss = bit_cost* distance
        api = connection.get_api()

        for message in api.get_messages(a):
            api.send_to(b, message)
        
        for message in api.get_messages(b):
            api.send_to(a, message)

        



    def validate_config(self, config):
        for key in self._needed_config:
            if key not in config:
                raise AttributeError("The config needs '{}'".format(key))
                
        
         
   