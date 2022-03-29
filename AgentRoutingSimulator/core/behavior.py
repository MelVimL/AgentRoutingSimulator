from abc import abstractmethod
from core.behaving import Behaving


class Behavior:
    """
    This class is for adding certein behavior to classes that inherents the
    Behaving class. Basicly it adds an update function to an
    Entity(like Agent or Connection).
    This makes all entitys in the Simulation customizable.
    All Behavior have access to the environment of the enity the behavior is
    attached to. It is recommendet to implement the
    """

    def __init__(self) -> None:
        self.enironment = {}

    @abstractmethod
    def update(self, time_step: int) -> None:
        pass

    def set_behaving(self, behaving: Behaving) -> None:
        self.behaving = behaving
