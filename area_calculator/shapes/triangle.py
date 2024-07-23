from math import isclose, sqrt

from .shape import Shape


class Triangle(Shape):
    """
    Triangle shape class.
    """

    def __init__(self, a, b, c):
        if a < 0 or b < 0 or c < 0:
            raise ValueError("Triangle's sides cannot be negative")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("The sides do not form a triangle")

        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = (self.a + self.b + self.c) / 2  # semi-perimeter
        area = sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))  # Herone's formula
        return area

    def is_right_angle(self):
        sides = sorted([self.a, self.b, self.c])
        return isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2)
