from __future__ import annotations

import sys
from collections.abc import Callable
from math import isclose

RealFunction = Callable[[float], float]

_CUBE_ROOT_EPS = sys.float_info.epsilon ** (1.0 / 3.0)


def _central_difference(func: RealFunction, t: float) -> float:
    step = _CUBE_ROOT_EPS * max(1.0, abs(t))
    return (func(t + step) - func(t - step)) / (2.0 * step)


def parametric_area(
    x_of_t: RealFunction,
    y_of_t: RealFunction,
    t_start: float,
    t_end: float,
    *,
    dx_dt: RealFunction | None = None,
    dy_dt: RealFunction | None = None,
    signed: bool = False,
    require_closed: bool = True,
    tolerance: float = 1e-10,
) -> float:
    if t_start == t_end:
        return 0.0
    if require_closed:
        closed = isclose(x_of_t(t_start), x_of_t(t_end), abs_tol=1e-9) and isclose(
            y_of_t(t_start), y_of_t(t_end), abs_tol=1e-9
        )
        if not closed:
            raise ValueError(
                "parametric curve is not closed; Green's-theorem area is undefined"
            )

    derivative_x = (
        dx_dt if dx_dt is not None else lambda t: _central_difference(x_of_t, t)
    )
    derivative_y = (
        dy_dt if dy_dt is not None else lambda t: _central_difference(y_of_t, t)
    )

    def integrand(t):
        return x_of_t(t) * derivative_y(t) - y_of_t(t) * derivative_x(t)

    from scipy.integrate import quad

    value, _ = quad(
        integrand, t_start, t_end, epsabs=tolerance, epsrel=tolerance, limit=200
    )
    signed_area = 0.5 * value
    return signed_area if signed else abs(signed_area)
