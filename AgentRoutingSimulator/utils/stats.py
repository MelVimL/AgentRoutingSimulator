class Stats:
    def __init__(self) -> None:
        self._stats = {}

    def get(self, name):
        return self._stats.setdefault(name, Stat(name))

    def __len__(self):
        return len(self._stats)


class Stat:

    def __init__(self, name) -> None:
        self._data = []
        self.name = name

    def gather(self, value):
        self._data.append(value)

    def values(self):
        return self._data
