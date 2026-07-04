from __future__ import annotations

from area_calculator.precision.backend import get_backend
from area_calculator.registry import register

from .shape import Solid


@register("sphere")
class Sphere(Solid):
    def __init__(self, radius, *, backend="float"):
        if radius < 0:
            raise ValueError("Sphere radius cannot be negative")
        self.radius = radius
        self._backend = get_backend(backend)

    def surface_area(self):
        backend = self._backend
        radius = backend.number(self.radius)
        return 4 * backend.pi * radius * radius

    def volume(self):
        backend = self._backend
        radius = backend.number(self.radius)
        return backend.number(4) / 3 * backend.pi * radius * radius * radius


@register("cylinder")
class Cylinder(Solid):
    def __init__(self, radius, height, *, backend="float"):
        if radius < 0 or height < 0:
            raise ValueError("Cylinder dimensions cannot be negative")
        self.radius = radius
        self.height = height
        self._backend = get_backend(backend)

    def surface_area(self):
        backend = self._backend
        radius = backend.number(self.radius)
        height = backend.number(self.height)
        return 2 * backend.pi * radius * (radius + height)

    def volume(self):
        backend = self._backend
        radius = backend.number(self.radius)
        height = backend.number(self.height)
        return backend.pi * radius * radius * height


@register("cone")
class Cone(Solid):
    def __init__(self, radius, height, *, backend="float"):
        if radius < 0 or height < 0:
            raise ValueError("Cone dimensions cannot be negative")
        self.radius = radius
        self.height = height
        self._backend = get_backend(backend)

    def slant_height(self):
        backend = self._backend
        radius = backend.number(self.radius)
        height = backend.number(self.height)
        return backend.sqrt(radius * radius + height * height)

    def surface_area(self):
        backend = self._backend
        radius = backend.number(self.radius)
        return backend.pi * radius * (radius + self.slant_height())

    def volume(self):
        backend = self._backend
        radius = backend.number(self.radius)
        height = backend.number(self.height)
        return backend.pi * radius * radius * height / 3
