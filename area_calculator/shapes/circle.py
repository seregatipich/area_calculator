from math import pi

from .shape import Shape


class Circle(Shape):
    """
    Circle shape class.
    """

    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius can't be negative")
        self.radius = radius

    def area(self):
        return pi * (self.radius**2)
