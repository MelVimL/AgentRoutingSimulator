from math import sqrt


class Position:
    
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def add(self, other):
        return Position(self.x+other.x, self.y+other.y)
    
    def sub(self, other):
        return Position(self.x-other.x, self.y-other.y)

    def distance(self, other):
        x = abs(self.x-other.x)
        y = abs(self.y-other.y)
        
        return sqrt(x**2+y**2)
    
    def scale(self, factor):
        return Position(self.x*factor, self.y*factor)
    
    def invert(self):
        return self.scale(-1.)


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
    
    def __contains__(self, position):
        pass


class Circle:
    
    def __init__(self, center, radius) -> None:
        self.radius = radius
        self.center = center
    
    def __contains__(self, position):
        return self.center.distance(position) <= self.radius