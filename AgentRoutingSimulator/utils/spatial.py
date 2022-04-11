from __future__ import annotations
from math import sqrt


def distance_of_agents(a, b):
    return a.get_position().distance(b.get_position())


class Position:

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def add(self, other: Position) -> Position:
        return Position(self.x+other.x, self.y+other.y)

    def sub(self, other: Position) -> Position:
        return Position(self.x-other.x, self.y-other.y)

    def distance(self, other: Position) -> float:
        x = abs(self.x-other.x)
        y = abs(self.y-other.y)

        return sqrt(x**2+y**2)

    def scale(self, factor: float) -> Position:
        return Position(self.x*factor, self.y*factor)

    def invert(self) -> Position:
        return self.scale(-1.)

    def to_tuple(self) -> tuple:
        return (self.x, self.y)


class Positions:

    ZERO = Position(.0, .0)
    UP = Position(.0, 1.)
    DOWN = UP.invert()
    RIGHT = Position(1., .0)
    LEFT = RIGHT.invert()
    DIAGONAL = Position(1., 1.)


class Quad:

    def __init__(self, left_top, bottom_right) -> None:
        self.top = left_top.y
        self.bottom = bottom_right.y
        self.right = bottom_right.x
        self.left = left_top.x

    def __contains__(self, position: Position):
        pass


class Circle:

    def __init__(self, center, radius) -> None:
        self.radius = radius
        self.center = center

    def __contains__(self, position):
        return self.center.distance(position) <= self.radius
