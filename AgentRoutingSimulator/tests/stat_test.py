import pytest
from simulation import SimpleSimulation
from factories import StatsFactory


@pytest.fixture
def _sim():
    return SimpleSimulation().simulation_key


def test_simple_stat(_sim):
    stats = StatsFactory.create(_sim)
    stat = stats.get("TestStat")
    stat.gather(1)
    stat.gather(2)
    stat.gather(3)

    values = stat.values()
    assert 3 == len(values)


def test_more_stats(_sim):
    test_1 = "Test1"
    test_2 = "Test2"
    stats = StatsFactory.create(_sim)
    old_len = len(stats)
    __ = stats.get(test_1).gather("Test1")
    __ = stats.get(test_2).gather("Test2")

    assert stats.get(test_1).values()[0][1] == "Test1"
    assert 2 == len(stats)-old_len
