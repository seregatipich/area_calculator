from __future__ import annotations

from math import pi, sin, tan

from area_calculator.precision.backend import get_backend
from area_calculator.registry import register

from .shape import Shape2D


@register("regular_polygon")
class RegularPolygon(Shape2D):
    """Regular n-gon defined by its side count and side length."""

    def __init__(self, num_sides, side_length, *, backend="float"):
        if not isinstance(num_sides, int) or num_sides < 3:
            raise ValueError("Regular polygon requires at least 3 sides")
        if side_length <= 0:
            raise ValueError("Side length must be positive")
        self.num_sides = num_sides
        self.side_length = side_length
        self._backend = get_backend(backend)

    def area(self):
        backend = self._backend
        n = backend.number(self.num_sides)
        side = backend.number(self.side_length)
        return n * side * side / (4 * backend.tan(backend.pi / n))

    def perimeter(self):
        backend = self._backend
        return backend.number(self.num_sides) * backend.number(self.side_length)

    def apothem(self):
        backend = self._backend
        n = backend.number(self.num_sides)
        return backend.number(self.side_length) / (2 * backend.tan(backend.pi / n))

    def circumradius(self):
        backend = self._backend
        n = backend.number(self.num_sides)
        return backend.number(self.side_length) / (2 * backend.sin(backend.pi / n))

    def interior_angle(self):
        backend = self._backend
        n = backend.number(self.num_sides)
        return (n - 2) * backend.pi / n

    @classmethod
    def from_circumradius(cls, num_sides, circumradius, *, backend="float"):
        side_length = 2 * circumradius * sin(pi / num_sides)
        return cls(num_sides, side_length, backend=backend)

    @classmethod
    def from_apothem(cls, num_sides, apothem, *, backend="float"):
        side_length = 2 * apothem * tan(pi / num_sides)
        return cls(num_sides, side_length, backend=backend)
