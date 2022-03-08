from simulation import SimpleSimulation
from utils.stats import Stats

def _sim():
    return SimpleSimulation().simulation_key

def test_simple_stat():
    stats = Stats(_sim())
    stat = stats.get("TestStat")
    stat.gather(1)
    stat.gather(2)
    stat.gather(3)

    assert 3 == len(stat.values())


def test_more_stats():
    stats = Stats(_sim())
    old_len = len(stats)
    stat1 = stats.get("Test1")
    stat2 = stats.get("Test2")

    assert 2 == len(stats)-old_len
