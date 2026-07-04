from __future__ import annotations

from math import pi, sqrt

from area_calculator.precision.backend import get_backend
from area_calculator.registry import register

from .shape import Shape2D


@register("ellipse")
class Ellipse(Shape2D):
    """Ellipse with an exact area and elliptic-integral perimeter."""

    def __init__(self, semi_major_axis, semi_minor_axis, *, backend="float"):
        if semi_major_axis <= 0 or semi_minor_axis <= 0:
            raise ValueError("Ellipse semi-axes must be positive")
        self.semi_major = max(semi_major_axis, semi_minor_axis)
        self.semi_minor = min(semi_major_axis, semi_minor_axis)
        self._backend = get_backend(backend)

    def area(self):
        backend = self._backend
        return (
            backend.pi
            * backend.number(self.semi_major)
            * backend.number(self.semi_minor)
        )

    def eccentricity(self) -> float:
        ratio = self.semi_minor / self.semi_major
        return sqrt(1.0 - ratio * ratio)

    def perimeter(self, method: str = "ellipe"):
        if method == "ellipe":
            return self._perimeter_ellipe()
        if method == "agm":
            return self.perimeter_agm()
        if method == "ramanujan":
            return self.perimeter_ramanujan()
        if method == "exact":
            return self._perimeter_exact()
        raise ValueError(f"Unknown perimeter method: {method}")

    def _perimeter_ellipe(self) -> float:
        from scipy.special import ellipe

        parameter = min(1.0, self.eccentricity() ** 2)
        return 4.0 * self.semi_major * float(ellipe(parameter))

    def perimeter_agm(self) -> float:
        current_a = 1.0
        current_b = self.semi_minor / self.semi_major
        difference = self.eccentricity()
        series_sum = 0.5 * difference * difference
        power = 0.5
        while abs(current_a - current_b) > 1e-16:
            next_a = (current_a + current_b) / 2.0
            next_b = sqrt(current_a * current_b)
            difference = (current_a - current_b) / 2.0
            current_a, current_b = next_a, next_b
            power *= 2.0
            series_sum += power * difference * difference
        complete_k = pi / (2.0 * current_a)
        complete_e = complete_k * (1.0 - series_sum)
        return 4.0 * self.semi_major * complete_e

    def perimeter_ramanujan(self) -> float:
        a, b = self.semi_major, self.semi_minor
        h = ((a - b) / (a + b)) ** 2
        return pi * (a + b) * (1.0 + (3.0 * h) / (10.0 + sqrt(4.0 - 3.0 * h)))

    def _perimeter_exact(self):
        import sympy

        semi_major = sympy.nsimplify(self.semi_major)
        parameter = sympy.nsimplify(self.eccentricity() ** 2)
        return 4 * semi_major * sympy.elliptic_e(parameter)
