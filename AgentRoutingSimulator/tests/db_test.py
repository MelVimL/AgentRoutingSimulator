import pytest
from db import get_session, Simulation

test_connection = "sqlite://"


def test_get_session():

    session = get_session(test_connection)
    sim = Simulation(name="Test")
    session.add(sim)
    session.commit()

    assert sim in session