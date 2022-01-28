from utils.stats import Stats
def test_simple_stat():
    stats = Stats()
    stat = stats.get("TestStat")

    stat.gather(1)
    stat.gather(2)
    stat.gather(3)

    assert 3 == len(stat.values())

def test_more_stats():
    stats = Stats()
    stat1 = stats.get("Test1")
    stat2 = stats.get("Test2")

    assert 2 == len(stats)