from math import hypot, sqrt
from collections import namedtuple


# ref: http://stackoverflow.com/questions/19458291/efficient-vector-point-class-in-python
class Vector2D(namedtuple('Vector2D', ('x', 'y'))):
    __slots__ = ()

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y))

    def __int__(self):
        return type(self)(int(self.x), int(self.y))

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return type(self)(self.x * other, self.y * other)

    def __div__(self, other):
        return type(self)(self.x / other, self.y / other)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def distance_to(self, other):
        """ uses the Euclidean norm to calculate the distance """
        return hypot((self.x - other.x), (self.y - other.y))

    @property
    def normalized(self):
        length = self.length
        if length == 0:
            return Vector2D(0, 0)
        return type(self)(self.x / length, self.y / length)

    @property
    def length_squared(self):
        return (self.x * self.x) + (self.y * self.y)

    @property
    def length(self):
        return sqrt(self.length_squared)

    def to_tuple(self):
        return self.x, self.y

def test():
    assert Vector2D(1, 0).distance_to(Vector2D(0, 0)) == 1
