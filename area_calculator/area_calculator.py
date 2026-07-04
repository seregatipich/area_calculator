from __future__ import annotations

from .shapes.shape import Number, Shape, Shape2D, Solid, SupportsArea


def calculate_area(shape: SupportsArea) -> Number:
    return shape.area()


def measure(shape: Shape) -> dict[str, Number]:
    measurements: dict[str, Number] = {"area": shape.area()}
    if isinstance(shape, Solid):
        measurements["surface_area"] = shape.surface_area()
        measurements["volume"] = shape.volume()
    elif isinstance(shape, Shape2D):
        measurements["perimeter"] = shape.perimeter()
    return measurements
