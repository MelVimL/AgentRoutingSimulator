import pytest
from db import get_session, Simulation, Stat, StatType

test_connection = "sqlite://"


def test_get_session():

    session = get_session(test_connection)
    sim = Simulation(name="Test")
    session.add(sim)
    session.commit()

    assert sim in session

def test_relationship_stat_type():

    session = get_session(test_connection)

    sim = Simulation(name="Test")
    stat_type = StatType(name="Test")
    stat = Stat(step=1, value={"Test":"test"}, stat_type=stat_type, simulation=sim)
    
    session.add(sim)
    session.commit()

    assert sim in session and stat in session and stat_type in session