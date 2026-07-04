from math import isclose

from area_calculator.numerical.heron import triangle_area
from area_calculator.precision.backend import get_backend
from area_calculator.precision.error import AreaEstimate, triangle_area_with_error
from area_calculator.precision.validate import validate_triangle_sides
from area_calculator.registry import register

from .shape import Shape2D


@register("triangle")
class Triangle(Shape2D):
    """Triangle shape class."""

    def __init__(self, a, b, c, *, backend="float"):
        validate_triangle_sides(a, b, c)
        self.a = a
        self.b = b
        self.c = c
        self._backend = get_backend(backend)

    def area(self):
        return triangle_area(self.a, self.b, self.c, self._backend)

    def perimeter(self):
        number = self._backend.number
        return number(self.a) + number(self.b) + number(self.c)

    def area_with_error(self) -> AreaEstimate:
        return triangle_area_with_error(self.a, self.b, self.c)

    def is_right_angle(self):
        sides = sorted([self.a, self.b, self.c])
        return isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2)
