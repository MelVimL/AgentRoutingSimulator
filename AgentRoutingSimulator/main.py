from __future__ import annotations
from tests.qrouting_test import send_messages
from tests.conftest import medium_sim_load, config_load
import cProfile
from pstats import Stats, SortKey


class Simulation:
    """
    """

    def __init__(self, config) -> None:

        pass

    def update() -> None:
        pass


def main():
    with cProfile.Profile() as pr:
        sim = medium_sim_load(config_load())
        agents = sim.get_agents()
        send_messages(10, agents)

        for i in range(1000):
            sim.update()

    Stats(pr).sort_stats(SortKey.TIME).reverse_order().print_stats()


if __name__ == "__main__":
    main()
