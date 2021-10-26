

from core.entities import Agent, Connection
from behavior.connections import Wireless


def test_simple_connection_behavior():
    a = Agent()
    b = Agent()
    connection = Connection(a, b)

    connection.add_behavior(Wireless(config={}))


def test_simple_connection_message_queue_in_out():
    a = Agent()
    b = Agent()
    connection = Connection(a, b)
    connection.send(a, bytes(20))
    connection.send(b, bytes(2000))

    connection.transfer_bytes(a, b, 20)
    connection.transfer_bytes(b, a, 1999)

    assert connection.has_message(b) and not connection.has_message(a)
