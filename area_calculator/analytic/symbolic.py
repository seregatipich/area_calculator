from __future__ import annotations

import math
from collections.abc import Sequence
from fractions import Fraction


def _is_perfect_square_fraction(value: Fraction) -> bool:
    numerator, denominator = value.numerator, value.denominator
    if numerator < 0:
        return False
    return (
        math.isqrt(numerator) ** 2 == numerator
        and math.isqrt(denominator) ** 2 == denominator
    )


def exact_triangle_area(a, b, c):
    largest, middle, smallest = sorted(
        (Fraction(a), Fraction(b), Fraction(c)), reverse=True
    )
    if smallest - (largest - middle) < 0:
        raise ValueError("The sides do not form a triangle")
    product = (
        (largest + (middle + smallest))
        * (smallest - (largest - middle))
        * (smallest + (largest - middle))
        * (largest + (middle - smallest))
    )
    area_squared = product / 16
    if _is_perfect_square_fraction(area_squared):
        root_numerator = math.isqrt(area_squared.numerator)
        root_denominator = math.isqrt(area_squared.denominator)
        return Fraction(root_numerator, root_denominator)
    import sympy

    return sympy.sqrt(sympy.Rational(area_squared.numerator, area_squared.denominator))


def exact_circle_area(radius):
    import sympy

    return sympy.pi * sympy.nsimplify(radius) ** 2


def symbolic_area_under_curve(expression, variable, a, b, *, simplify: bool = True):
    import sympy

    result = sympy.integrate(expression, (variable, a, b))
    if result.has(sympy.Integral):
        raise ValueError(
            "no closed-form antiderivative; use area_under_curve for a numeric result"
        )
    if result.is_finite is False:
        raise ValueError("the integral does not converge")
    return sympy.simplify(result) if simplify else result


def exact_polygon_area(vertices: Sequence[tuple]) -> Fraction:
    if len(vertices) < 3:
        raise ValueError("a polygon needs at least three vertices")
    total = Fraction(0)
    count = len(vertices)
    for index in range(count):
        x_i, y_i = vertices[index]
        x_j, y_j = vertices[(index + 1) % count]
        for coordinate in (x_i, y_i, x_j, y_j):
            if isinstance(coordinate, float):
                raise TypeError(
                    "exact_polygon_area requires Fraction or int coordinates"
                )
        total += Fraction(x_i) * Fraction(y_j) - Fraction(x_j) * Fraction(y_i)
    return abs(total) / 2


def as_float(expression) -> float:
    import sympy

    return float(sympy.N(expression))


def symbolic_matches_numeric(exact, numeric: float, *, rel_tol: float = 1e-9) -> bool:
    return math.isclose(as_float(exact), numeric, rel_tol=rel_tol, abs_tol=1e-12)
