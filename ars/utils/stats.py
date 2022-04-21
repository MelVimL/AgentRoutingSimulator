from __future__ import annotations
from ..db.api import SimulationAPI as sim_db
from ..db.api import StatsAPI as db


class Stats:
    """
    """

    def __init__(self, simulation_id: int) -> None:
        """
        """
        self._simulation_id = simulation_id

    def get(self, name: str) -> Stat:
        """
        """
        stat_type_id = db.get_stat_type_from_name(name)
        if not stat_type_id:
            db.create_stat_type(name)
            stat_type_id = db.get_stat_type_from_name(name)

        return Stat(stat_type_id=stat_type_id,
                    simulation_id=self._simulation_id)

    def __len__(self):
        return len(db.get_stat_types())


class Stat:
    """
    """

    def __init__(self, stat_type_id: int, simulation_id: int) -> None:
        """
        """
        self.simulation_id = simulation_id
        self.stat_type_id = stat_type_id

    def gather(self, value: any):
        """
        """
        db.add_stat(simulation_id=self.simulation_id,
                    stat_type_id=self.stat_type_id,
                    time_step=sim_db.get_time_step(self.simulation_id),
                    value=value)
        # self._data.append(value)

    def values(self) -> any:
        """
        """
        return db.get_stats(self.simulation_id, self.stat_type_id)
