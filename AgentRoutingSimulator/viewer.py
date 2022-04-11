from db.api import init_session
from db.api import SimulationAPI
from db.api import StatsAPI


def search_for_stat_types(sim):
    like = str(input("Type name like: "))
    stat_types = StatsAPI.get_stat_type_like(like)

    for index, stat_type in enumerate(stat_types):
        print("f{index}: {stat_type.name}")

    index = int(input("Which Type?"))
    return index


def select_sims_cmd():
    simulations = SimulationAPI.get_simulations()
    for index, simulation in enumerate(simulations):
        print("f{index}: {simulation.name}")

    index = int(input("Which simulation?"))

    return index


def main():
    db_str = str(input("Database Connectionstring:"))
    init_session(db_str)
    sim = select_sims_cmd()


if __name__ == "__main__":
    main()
