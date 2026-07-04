from __future__ import annotations

from math import atan, pi, sqrt, tan

from area_calculator.registry import register

from .shape import Shape


@register("spherical_triangle")
class SphericalTriangle(Shape):
    """Triangle on a sphere; area from the spherical excess."""

    def __init__(self, side_a, side_b, side_c, radius=1.0):
        if radius <= 0:
            raise ValueError("Sphere radius must be positive")
        for side in (side_a, side_b, side_c):
            if not 0 < side < pi:
                raise ValueError("Each spherical side must lie in (0, pi)")
        if side_a + side_b + side_c >= 2 * pi:
            raise ValueError("The arcs do not form a spherical triangle")
        largest, middle, smallest = sorted((side_a, side_b, side_c), reverse=True)
        if largest >= middle + smallest:
            raise ValueError("The arcs do not form a spherical triangle")
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
        self.radius = radius
        self._excess = None

    def spherical_excess(self) -> float:
        if self._excess is not None:
            return self._excess
        semi = (self.side_a + self.side_b + self.side_c) / 2.0
        product = (
            tan(semi / 2.0)
            * tan((semi - self.side_a) / 2.0)
            * tan((semi - self.side_b) / 2.0)
            * tan((semi - self.side_c) / 2.0)
        )
        return 4.0 * atan(sqrt(max(product, 0.0)))

    def area(self):
        return self.radius**2 * self.spherical_excess()

    @classmethod
    def from_angles(cls, angle_a, angle_b, angle_c, radius=1.0):
        excess = (angle_a + angle_b + angle_c) - pi
        if not 0 < excess < 2 * pi:
            raise ValueError("Angle sum must exceed pi for a spherical triangle")
        instance = cls.__new__(cls)
        instance.side_a = None
        instance.side_b = None
        instance.side_c = None
        instance.radius = radius
        instance._excess = excess
        return instance
