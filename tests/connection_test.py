import json

from ars.core.entities import Agent, Connection
from ars.behavior.connections import Wireless


def test_simple_connection_behavior():
    a = Agent()
    b = Agent()
    connection = Connection(a, b)

    connection.add_behavior(Wireless(config={}))


def test_simple_connection_message_queue_in_out():
    a = Agent()
    b = Agent()
    message_a = {"test_message": "test"}
    message_b = {"test_message": "test"*500}
    connection = Connection(a, b)
    connection.send(a, message_a)
    connection.send(b, message_b)

    connection.transfer_bytes(a, b, len(json.dumps(message_a)))
    connection.transfer_bytes(b, a, len(json.dumps(message_b))-1)

    assert connection.has_message(b) and not connection.has_message(a)
