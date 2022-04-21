from datetime import datetime as dt
from .schema import Base, StatType, Stat, Simulation
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

DEFAULT_DB = "sqlite://"
_engine = None


def one_or_none(result):
    if result:
        result = result[0]
    return result


def init_session(connection_string=DEFAULT_DB):
    global _engine
    _engine = create_engine(connection_string, encoding="UTF-8", echo=True)
    Base.metadata.create_all(_engine)


def get_session(connection_string=DEFAULT_DB):
    if not _engine and connection_string:
        init_session(connection_string)
    return Session(_engine)


class SimulationAPI():
    @staticmethod
    def create_simulation(name, config) -> int:
        simulation = Simulation(name=name, config=config,
                                start_datetime=dt.now(), current_time_step=0)

        with get_session() as session, session.begin():
            session.add(simulation)

        return SimulationAPI.get_simulation_id(name)

    @staticmethod
    def get_simulation_id(name):
        with get_session() as session, session.begin():
            statement = select(Simulation).where(Simulation.name == name)
            result = session.execute(statement).first()
            return result[0].id

    @staticmethod
    def get_time_step(simulation_id: int) -> int:
        with get_session() as session, session.begin():
            statement = select(Simulation).where(
                Simulation.id == simulation_id)
            return session.execute(statement).first()[0].current_time_step

    @staticmethod
    def set_time_step(simulation_id: int, time_step) -> None:
        with get_session() as session:
            with session.begin():
                statement = update(Simulation)\
                    .where(Simulation.id == simulation_id)\
                    .values(current_time_step=time_step)
                session.execute(statement)


class StatsAPI:

    @staticmethod
    def create_stat_type(name):
        with get_session() as session, session.begin():
            session.add(StatType(name=name))

    @staticmethod
    def get_stat_type_from_name(name):
        with get_session() as session, session.begin():
            statement = select(StatType).where(StatType.name == name)
            result = session.execute(statement).first()
            if result:
                result = result[0].id
            return result

    @staticmethod
    def get_stat_type_like(like):
        with get_session() as session, session.begin():
            statement = select(StatType).where(StatType.name.like(like))
            result = session.execute(statement).all()
            return result

    @staticmethod
    def get_stat_type(id):
        with get_session() as session, session.begin():
            statement = select(StatType).where(StatType.id == id)
            return session.execute(statement).first()[0]

    @staticmethod
    def get_stat_types():
        with get_session() as session, session.begin():
            statement = select(StatType)
            return session.execute(statement).all()

    @staticmethod
    def add_stat(simulation_id: int, stat_type_id: int, time_step: int, value):
        stat = Stat(simulation_id=simulation_id,
                    stat_type_id=stat_type_id, step=time_step, value=value)
        with get_session() as session, session.begin():
            session.add(stat)

    @staticmethod
    def get_stats(simulation_id: int, stat_type_id: int,):
        with get_session() as session, session.begin():
            statement = select(Stat)\
                .where(Simulation.id == simulation_id)\
                .where(StatType.id == stat_type_id)\
                .order_by(Stat.step)
            return [(x.step, x.value) for x in session.execute(statement).scalars().all()]
