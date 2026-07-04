from area_calculator.precision.backend import get_backend
from area_calculator.registry import register

from .shape import Shape2D


@register("circle")
class Circle(Shape2D):
    """Circle shape class."""

    def __init__(self, radius, *, backend="float"):
        if radius < 0:
            raise ValueError("Radius can't be negative")
        self.radius = radius
        self._backend = get_backend(backend)

    def area(self):
        return self._backend.pi * self._backend.number(self.radius) ** 2

    def perimeter(self):
        return 2 * self._backend.pi * self._backend.number(self.radius)
