from __future__ import annotations

from collections.abc import Sequence

from area_calculator.geometry.predicates import Point, segments_intersect


def find_self_intersections(vertices: Sequence[Point]) -> list[tuple[int, int]]:
    count = len(vertices)
    if count < 3:
        raise ValueError("A polygon needs at least three vertices")
    edges = [(vertices[i], vertices[(i + 1) % count]) for i in range(count)]
    crossings = []
    for i in range(count):
        for j in range(i + 1, count):
            if j == i + 1 or (i == 0 and j == count - 1):
                continue
            a, b = edges[i]
            c, d = edges[j]
            if segments_intersect(a, b, c, d):
                crossings.append((i, j))
    return crossings


def is_simple_polygon(vertices: Sequence[Point]) -> bool:
    return not find_self_intersections(vertices)
