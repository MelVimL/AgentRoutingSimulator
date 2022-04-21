from __future__ import annotations
from tests.qrouting_test import send_messages
from tests.conftest import medium_sim_load
from utils.config import ConfigLoader
from json import dump
from factories import StatsFactory

PATH_DUMP = "/data/q_routing"


def get_data():
    stats = StatsFactory.create()
    arival_times = [x for x in stats.get("message_arrival_time").values()]
    result = {}
    for x, y in arival_times:
        result.setdefault(x, []).append(y)

    xs = [x for x in result]
    ys = [sum(result[y])/len(result[y]) for y in xs]
    return (xs, ys)


def dump_data(sim):
    data = get_data()
    with open(f"{PATH_DUMP}/{sim.name}.json", "w+") as f:
        dump(data, fp=f)


def main():
    #path = input("path to config: ")
    config = ConfigLoader.load("/opt/conf/config.yaml")

    sim = medium_sim_load(config)

    agents = sim.get_agents()
    for i in range(5):
        send_messages(100, agents)
        for i in range(2000):
            sim.update()
    dump_data(sim)


if __name__ == "__main__":
    main()
