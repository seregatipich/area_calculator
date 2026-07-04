from __future__ import annotations

import math


def require_finite(name: str, value) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")


def require_non_negative(name: str, value, message: str | None = None) -> None:
    if value < 0:
        raise ValueError(message or f"{name} cannot be negative")


def validate_radius(radius) -> None:
    require_finite("radius", radius)
    if radius < 0:
        raise ValueError("Radius can't be negative")


def validate_triangle_sides(a, b, c) -> None:
    for name, value in (("a", a), ("b", b), ("c", c)):
        require_finite(name, value)
    if a < 0 or b < 0 or c < 0:
        raise ValueError("Triangle's sides cannot be negative")
    largest, middle, smallest = sorted((a, b, c), reverse=True)
    if smallest - (largest - middle) <= 0:
        raise ValueError("The sides do not form a triangle")
