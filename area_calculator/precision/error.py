from __future__ import annotations

import sys
from dataclasses import dataclass

_EPS = sys.float_info.epsilon
_KAHAN_OP_COUNT = 8.0


@dataclass(frozen=True)
class AreaEstimate:
    value: float
    absolute_error_bound: float
    relative_error_bound: float
    condition_number: float


def triangle_area_with_error(a: float, b: float, c: float) -> AreaEstimate:
    from area_calculator.numerical.heron import kahan_triangle_area

    value = kahan_triangle_area(a, b, c)
    largest, middle, smallest = sorted((a, b, c), reverse=True)
    denominator = smallest - (largest - middle)
    if denominator <= 0:
        raise ValueError("The sides do not form a triangle")
    condition_number = largest / denominator
    relative_error_bound = condition_number * _EPS * _KAHAN_OP_COUNT
    absolute_error_bound = relative_error_bound * value
    return AreaEstimate(
        value=value,
        absolute_error_bound=absolute_error_bound,
        relative_error_bound=relative_error_bound,
        condition_number=condition_number,
    )
