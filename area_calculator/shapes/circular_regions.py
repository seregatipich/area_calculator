from __future__ import annotations

from math import pi, sin

from area_calculator.precision.backend import get_backend
from area_calculator.registry import register

from .shape import Shape2D


@register("annulus")
class Annulus(Shape2D):
    """Ring between two concentric circles."""

    def __init__(self, outer_radius, inner_radius, *, backend="float"):
        if outer_radius < 0 or inner_radius < 0:
            raise ValueError("Annulus radii cannot be negative")
        if outer_radius < inner_radius:
            raise ValueError("Annulus outer radius must be >= inner radius")
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self._backend = get_backend(backend)

    def area(self):
        backend = self._backend
        outer = backend.number(self.outer_radius)
        inner = backend.number(self.inner_radius)
        return backend.pi * (outer - inner) * (outer + inner)

    def perimeter(self):
        backend = self._backend
        outer = backend.number(self.outer_radius)
        inner = backend.number(self.inner_radius)
        return 2 * backend.pi * (outer + inner)


@register("circular_sector")
class CircularSector(Shape2D):
    """Pie-slice region bounded by two radii and an arc."""

    def __init__(self, radius, central_angle, *, backend="float"):
        if radius <= 0:
            raise ValueError("Sector radius must be positive")
        if not 0 <= central_angle <= 2 * pi:
            raise ValueError("Central angle must be between 0 and 2*pi")
        self.radius = radius
        self.central_angle = central_angle
        self._backend = get_backend(backend)

    def arc_length(self):
        backend = self._backend
        return backend.number(self.radius) * backend.number(self.central_angle)

    def area(self):
        backend = self._backend
        radius = backend.number(self.radius)
        angle = backend.number(self.central_angle)
        return radius * radius * angle / 2

    def perimeter(self):
        backend = self._backend
        return 2 * backend.number(self.radius) + self.arc_length()


@register("circular_segment")
class CircularSegment(Shape2D):
    """Region between a chord and its arc."""

    def __init__(self, radius, central_angle):
        if radius <= 0:
            raise ValueError("Segment radius must be positive")
        if not 0 <= central_angle <= 2 * pi:
            raise ValueError("Central angle must be between 0 and 2*pi")
        self.radius = radius
        self.central_angle = central_angle

    def _theta_minus_sin(self, theta: float) -> float:
        if theta < 1e-2:
            return theta**3 / 6.0 - theta**5 / 120.0 + theta**7 / 5040.0
        return theta - sin(theta)

    def area(self):
        return 0.5 * self.radius**2 * self._theta_minus_sin(self.central_angle)

    def chord_length(self):
        return 2.0 * self.radius * sin(self.central_angle / 2.0)

    def sagitta(self):
        return self.radius * 2.0 * sin(self.central_angle / 4.0) ** 2

    def perimeter(self):
        return self.chord_length() + self.radius * self.central_angle
