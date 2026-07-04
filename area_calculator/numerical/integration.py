from __future__ import annotations

import math
from collections.abc import Callable, Sequence

RealFunction = Callable[[float], float]


def _adaptive(func, a, b, fa, fb, fm, whole, tolerance, depth):
    midpoint = (a + b) / 2.0
    left_mid = (a + midpoint) / 2.0
    right_mid = (midpoint + b) / 2.0
    f_left_mid = func(left_mid)
    f_right_mid = func(right_mid)
    if not (math.isfinite(f_left_mid) and math.isfinite(f_right_mid)):
        raise ValueError("integrand returned a non-finite value")
    left = (midpoint - a) / 6.0 * (fa + 4.0 * f_left_mid + fm)
    right = (b - midpoint) / 6.0 * (fm + 4.0 * f_right_mid + fb)
    delta = left + right - whole
    if depth <= 0 or abs(delta) <= 15.0 * tolerance:
        return left + right + delta / 15.0
    return _adaptive(
        func, a, midpoint, fa, fm, f_left_mid, left, tolerance / 2.0, depth - 1
    ) + _adaptive(
        func, midpoint, b, fm, fb, f_right_mid, right, tolerance / 2.0, depth - 1
    )


def adaptive_simpson(
    func: RealFunction,
    a: float,
    b: float,
    *,
    tolerance: float = 1e-10,
    max_depth: int = 50,
) -> float:
    if a == b:
        return 0.0
    fa = func(a)
    fb = func(b)
    fm = func((a + b) / 2.0)
    whole = (b - a) / 6.0 * (fa + 4.0 * fm + fb)
    return _adaptive(func, a, b, fa, fb, fm, whole, tolerance, max_depth)


def area_under_curve(
    func: RealFunction,
    a: float,
    b: float,
    *,
    method: str = "quad",
    tolerance: float = 1e-10,
    max_depth: int = 50,
) -> float:
    if a == b:
        return 0.0
    if method == "quad":
        from scipy.integrate import quad

        value, _ = quad(func, a, b, epsabs=tolerance, epsrel=tolerance, limit=200)
        return value
    if method == "simpson":
        return adaptive_simpson(func, a, b, tolerance=tolerance, max_depth=max_depth)
    raise ValueError(f"Unknown integration method: {method}")


def area_between_curves(
    upper: RealFunction,
    lower: RealFunction,
    a: float,
    b: float,
    *,
    absolute: bool = False,
    method: str = "quad",
    tolerance: float = 1e-10,
    breakpoints: Sequence[float] = (),
) -> float:
    if not absolute:
        return area_under_curve(
            lambda x: upper(x) - lower(x), a, b, method=method, tolerance=tolerance
        )

    def integrand(x):
        return abs(upper(x) - lower(x))

    if method == "quad":
        from scipy.integrate import quad

        value, _ = quad(
            integrand,
            a,
            b,
            epsabs=tolerance,
            epsrel=tolerance,
            points=tuple(breakpoints) or None,
            limit=200,
        )
        return value
    bounds = [a, *breakpoints, b]
    return math.fsum(
        adaptive_simpson(integrand, bounds[i], bounds[i + 1], tolerance=tolerance)
        for i in range(len(bounds) - 1)
    )
