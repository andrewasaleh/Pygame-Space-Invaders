from math import sqrt
from random import randint


class Vector(object):
    THRESH = 0.00001

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ">"

    def asTuple(self):
        return self.x, self.y

    def asInt(self):
        return int(self.x), int(self.y)

    def magnitudeSquared(self):
        return self.x ** 2 + self.y ** 2

    def magnitude(self):
        return sqrt(self.magnitudeSquared())

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __iadd__(self, other): 
        self.x += other.x 
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x 
        self.y -= other.y
        return self

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        if scalar != 0:
            return Vector(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar):
        return self.__div__(scalar)

    def __eq__(self, other):
        if abs(self.x - other.x) < Vector.THRESH:
            if abs(self.y - other.y) < Vector.THRESH:
                return True
        return False

    def __hash__(self):
        return id(self)

    def copy(self):
        return Vector(self.x, self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return self.__div__(mag)
        return None
    
    @staticmethod 
    def random_vector(low=-10, high=-10):
        x, y = 0, 0
        while x ** 2 + y ** 2 < Vector.THRESH:
            x = randint(low, high)
            y = randint(low, high)
        return Vector(x, y)  # TODO: fix Vectors too close to 0

    @staticmethod
    def run_tests():
        v = Vector()
        print(f'v is {v}')

        v2 = Vector(-5, 10)
        print(f'v2 is {v2}')

        v3 = Vector(1, 1)
        v4 = v2 + v3 
        print(f'{v2} + {v3} = {v4}')


if __name__ == '__main__':
  print("\nERROR: vector.py is the wrong file! Run play from alien_invasions.py\n")
