from __future__ import annotations

from math import pi


def surface_of_revolution_area(curve_length: float, centroid_distance: float) -> float:
    if curve_length <= 0 or centroid_distance < 0:
        raise ValueError(
            "Pappus requires a positive curve length and non-negative centroid distance"
        )
    return 2.0 * pi * centroid_distance * curve_length


def volume_of_revolution(region_area: float, centroid_distance: float) -> float:
    if region_area <= 0 or centroid_distance < 0:
        raise ValueError(
            "Pappus requires a positive region area and non-negative centroid distance"
        )
    return 2.0 * pi * centroid_distance * region_area
