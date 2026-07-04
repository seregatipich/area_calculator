from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from math import sqrt

Indicator = Callable[[float, float], bool]
BoundingBox = tuple[float, float, float, float]


@dataclass(frozen=True)
class MonteCarloArea:
    estimate: float
    standard_error: float
    confidence_interval: tuple[float, float]
    confidence_level: float
    n_samples: int
    hits: int


def _z_value(confidence_level: float) -> float:
    try:
        from scipy.stats import norm

        return float(norm.ppf(0.5 + confidence_level / 2.0))
    except ImportError:
        from statistics import NormalDist

        return NormalDist().inv_cdf(0.5 + confidence_level / 2.0)


def monte_carlo_area(
    indicator: Indicator,
    bounds: BoundingBox,
    *,
    n_samples: int = 1_000_000,
    seed: int | None = None,
    confidence_level: float = 0.95,
    interval: str = "wilson",
) -> MonteCarloArea:
    x_min, x_max, y_min, y_max = bounds
    if x_min > x_max or y_min > y_max:
        raise ValueError("bounds must satisfy x_min <= x_max and y_min <= y_max")
    box_area = (x_max - x_min) * (y_max - y_min)
    if box_area == 0:
        raise ValueError("bounding box has zero area")
    if n_samples <= 0:
        raise ValueError("n_samples must be positive")

    import numpy as np

    rng = np.random.default_rng(seed)
    xs = rng.uniform(x_min, x_max, n_samples)
    ys = rng.uniform(y_min, y_max, n_samples)
    hits = sum(1 for x, y in zip(xs, ys) if indicator(x, y))
    proportion = hits / n_samples
    estimate = proportion * box_area
    standard_error = box_area * sqrt(proportion * (1.0 - proportion) / n_samples)
    z = _z_value(confidence_level)

    if interval == "normal":
        low = estimate - z * standard_error
        high = estimate + z * standard_error
    elif interval == "wilson":
        denominator = 1.0 + z * z / n_samples
        center = (proportion + z * z / (2.0 * n_samples)) / denominator
        half_width = (z / denominator) * sqrt(
            proportion * (1.0 - proportion) / n_samples
            + z * z / (4.0 * n_samples * n_samples)
        )
        low = (center - half_width) * box_area
        high = (center + half_width) * box_area
    else:
        raise ValueError(f"Unknown interval type: {interval}")

    return MonteCarloArea(
        estimate=estimate,
        standard_error=standard_error,
        confidence_interval=(low, high),
        confidence_level=confidence_level,
        n_samples=n_samples,
        hits=hits,
    )
