

from core.entities import Agent, Connection
from behavior.connections import Wireless


def test_simple_connection_behavior():
    a = Agent()
    b = Agent()
    connection = Connection(a, b)

    connection.add_behavior(Wireless(config={}))

def test_simple_connection_message_queue_in():
    a = Agent()
    b = Agent()
    connection = Connection(a, b)

    #in_queue = connection.get_in_queue()
    #out_queue = connection.get_in_queue()
    