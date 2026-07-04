from __future__ import annotations

from collections.abc import Sequence
from math import asin, cos, pi, sin, sqrt

from area_calculator.registry import register

from .shape import Shape2D


@register("quadrilateral")
class Quadrilateral(Shape2D):
    """General quadrilateral via Bretschneider's formula."""

    def __init__(self, a, b, c, d, angle_sum=None):
        for side in (a, b, c, d):
            if side <= 0:
                raise ValueError("Quadrilateral sides must be positive")
        longest = max(a, b, c, d)
        if longest >= (a + b + c + d) - longest:
            raise ValueError("The sides do not form a quadrilateral")
        self.a, self.b, self.c, self.d = a, b, c, d
        self.angle_sum = pi if angle_sum is None else angle_sum

    def perimeter(self):
        return self.a + self.b + self.c + self.d

    def area(self):
        s = self.perimeter() / 2
        half_angle = self.angle_sum / 2
        radicand = (s - self.a) * (s - self.b) * (s - self.c) * (s - self.d) - (
            self.a * self.b * self.c * self.d * cos(half_angle) ** 2
        )
        return sqrt(max(radicand, 0.0))

    @classmethod
    def cyclic(cls, a, b, c, d):
        return cls(a, b, c, d, angle_sum=pi)


def cyclic_polygon_area(sides: Sequence[float]) -> float:
    if len(sides) < 3:
        raise ValueError("A polygon needs at least three sides")
    longest = max(sides)
    if longest >= sum(sides) - longest:
        raise ValueError("The sides do not form a cyclic polygon")

    from scipy.optimize import brentq

    def central_angle_excess(radius: float) -> float:
        total = sum(2.0 * asin(min(1.0, side / (2.0 * radius))) for side in sides)
        return total - 2.0 * pi

    lower = longest / 2.0
    radius_low = lower * (1.0 + 1e-12)
    radius_high = lower * 2.0
    while central_angle_excess(radius_high) > 0:
        radius_high *= 2.0
    radius = brentq(central_angle_excess, radius_low, radius_high)
    return sum(
        0.5 * radius**2 * sin(2.0 * asin(min(1.0, side / (2.0 * radius))))
        for side in sides
    )
