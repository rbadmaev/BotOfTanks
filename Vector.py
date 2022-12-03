from copy import copy
import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, other):
        if isinstance( other, float):
            self.x += other
            self.y += other

        elif isinstance(other, Vector):
            self.x += other.x
            self.y += other.y

        elif isinstance(other, tuple) and len(other) == 2:
            self.x += other[0]
            self.y += other[1]

        else:
            raise Exception("Unknown term type")

        return self

    def __add__(self, other):
        result = copy(self)
        result += other
        return result

    def __isub__(self, other):
        if isinstance( other, float):
            self.x -= other
            self.y -= other

        elif isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y

        elif isinstance(other, tuple) and len(other) == 2:
            self.x -= other[0]
            self.y -= other[1]

        else:
            raise Exception("Unknown term type")

        return self

    def __sub__(self, other):
        result = copy(self)
        result -= other
        return result

    def __imul__(self, right: float):
        self.x *= right
        self.y *= right
        return self

    def __mul__(self, right: float):
        result = copy(self)
        result *= right
        return result

    def __itruediv__(self, right: float):
        self.x /= right
        self.y /= right
        return self

    def __truediv__(self, right: float):
        result = copy(self)
        result /= right
        return result

    def getAngle(self, default: float):
        if self.x == 0:
            if self.y > 0:
                return math.pi/2
            if self.y < 0:
                return math.pi*3/2
            else:
                return default

        return math(atan(self.y / self.x))

    def lenght(self) -> float:
        return math.sqrt(self.x*self.x + self.y*self.y)

    def shorten(self, lenght: float):
        result = copy(self)
        selfLen = self.lenght()
        if (lenght < selfLen):
            result *= lenght / selfLen

        return result

    def resize(self, lenght: float):
        result = copy(self)
        result *= lenght / self.lenght()
        return result

    def getJsonStruct(self):
        return [self.x, self.y]

    def __repr__(self):
        return "[x=" + str(self.x) + ", y=" + str(self.y) + "]"
