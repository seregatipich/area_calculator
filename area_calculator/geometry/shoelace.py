from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Literal

from area_calculator.geometry.predicates import Point, orient, point_on_segment


def _require_polygon(vertices: Sequence[Point]) -> None:
    if len(vertices) < 3:
        raise ValueError("A polygon needs at least three vertices")


def signed_area(vertices: Sequence[Point]) -> float:
    _require_polygon(vertices)
    origin_x, origin_y = vertices[0]
    count = len(vertices)
    terms = []
    for index in range(count):
        x_i, y_i = vertices[index]
        x_j, y_j = vertices[(index + 1) % count]
        terms.append(
            (x_i - origin_x) * (y_j - origin_y) - (x_j - origin_x) * (y_i - origin_y)
        )
    return 0.5 * math.fsum(terms)


def polygon_area(vertices: Sequence[Point]) -> float:
    return abs(signed_area(vertices))


def orientation(vertices: Sequence[Point]) -> Literal["CCW", "CW", "DEGENERATE"]:
    area = signed_area(vertices)
    if area > 0:
        return "CCW"
    if area < 0:
        return "CW"
    return "DEGENERATE"


def perimeter(vertices: Sequence[Point]) -> float:
    _require_polygon(vertices)
    count = len(vertices)
    edges = []
    for index in range(count):
        x_i, y_i = vertices[index]
        x_j, y_j = vertices[(index + 1) % count]
        edges.append(math.hypot(x_j - x_i, y_j - y_i))
    return math.fsum(edges)


def centroid(vertices: Sequence[Point]) -> Point:
    _require_polygon(vertices)
    origin_x, origin_y = vertices[0]
    count = len(vertices)
    cross_terms, weighted_x, weighted_y = [], [], []
    for index in range(count):
        x_i = vertices[index][0] - origin_x
        y_i = vertices[index][1] - origin_y
        x_j = vertices[(index + 1) % count][0] - origin_x
        y_j = vertices[(index + 1) % count][1] - origin_y
        cross = x_i * y_j - x_j * y_i
        cross_terms.append(cross)
        weighted_x.append((x_i + x_j) * cross)
        weighted_y.append((y_i + y_j) * cross)
    doubled_area = math.fsum(cross_terms)
    if doubled_area == 0:
        mean_x = math.fsum(vertex[0] for vertex in vertices) / count
        mean_y = math.fsum(vertex[1] for vertex in vertices) / count
        return (mean_x, mean_y)
    centroid_x = math.fsum(weighted_x) / (3 * doubled_area) + origin_x
    centroid_y = math.fsum(weighted_y) / (3 * doubled_area) + origin_y
    return (centroid_x, centroid_y)


def contains_point(
    vertices: Sequence[Point],
    point: Point,
    *,
    include_boundary: bool = True,
    method: Literal["winding", "ray"] = "winding",
) -> bool:
    _require_polygon(vertices)
    count = len(vertices)
    for index in range(count):
        if point_on_segment(point, vertices[index], vertices[(index + 1) % count]):
            return include_boundary
    if method == "winding":
        return _winding_number(vertices, point) != 0
    if method == "ray":
        return _ray_crossing(vertices, point)
    raise ValueError(f"Unknown method: {method}")


def _winding_number(vertices: Sequence[Point], point: Point) -> int:
    count = len(vertices)
    _, point_y = point
    winding = 0
    for index in range(count):
        a = vertices[index]
        b = vertices[(index + 1) % count]
        if a[1] <= point_y:
            if b[1] > point_y and orient(a, b, point) > 0:
                winding += 1
        else:
            if b[1] <= point_y and orient(a, b, point) < 0:
                winding -= 1
    return winding


def _ray_crossing(vertices: Sequence[Point], point: Point) -> bool:
    count = len(vertices)
    point_x, point_y = point
    inside = False
    for index in range(count):
        a = vertices[index]
        b = vertices[(index + 1) % count]
        if (a[1] > point_y) != (b[1] > point_y):
            x_cross = a[0] + (point_y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if point_x < x_cross:
                inside = not inside
    return inside
