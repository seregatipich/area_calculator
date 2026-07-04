from __future__ import annotations

from math import sqrt

from area_calculator.precision.backend import Backend, Precision, get_backend


def kahan_triangle_area(a: float, b: float, c: float) -> float:
    a, b, c = sorted((a, b, c), reverse=True)
    if c - (a - b) < 0:
        raise ValueError("The sides do not form a triangle")
    product = (a + (b + c)) * (c - (a - b)) * (c + (a - b)) * (a + (b - c))
    return 0.25 * sqrt(product)


def triangle_area(a, b, c, precision: str | Precision | Backend = Precision.FLOAT):
    backend = get_backend(precision)
    x, y, z = (backend.number(side) for side in sorted((a, b, c), reverse=True))
    if z - (x - y) < 0:
        raise ValueError("The sides do not form a triangle")
    product = (x + (y + z)) * (z - (x - y)) * (z + (x - y)) * (x + (y - z))
    return backend.sqrt(product) / 4
