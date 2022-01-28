from __future__ import annotations


class Stats:
    """
    """
    def __init__(self) -> None:
        """
        """
        self._stats = {}

    def get(self, name: str) -> Stat:
        """
        """
        return self._stats.setdefault(name, Stat(name))

    def __len__(self):
        return len(self._stats)


class Stat:
    """
    """
    def __init__(self, name: str) -> None:
        """
        """
        self._data = []
        self.name = name

    def gather(self, value: any):
        """
        """
        self._data.append(value)

    def values(self) -> any:
        """
        """
        return self._data
