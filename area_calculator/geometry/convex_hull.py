from __future__ import annotations

from collections.abc import Sequence

from area_calculator.geometry.predicates import Point, orient
from area_calculator.geometry.shoelace import polygon_area


def _turn_removes(o: Point, a: Point, b: Point, include_collinear: bool) -> bool:
    cross = orient(o, a, b)
    return cross < 0 if include_collinear else cross <= 0


def convex_hull(
    points: Sequence[Point], *, include_collinear: bool = False
) -> list[Point]:
    unique = sorted({tuple(point) for point in points})
    if len(unique) <= 2:
        return unique

    def build(ordered: list[Point]) -> list[Point]:
        chain: list[Point] = []
        for point in ordered:
            while len(chain) >= 2 and _turn_removes(
                chain[-2], chain[-1], point, include_collinear
            ):
                chain.pop()
            chain.append(point)
        return chain

    lower = build(unique)
    upper = build(unique[::-1])
    return lower[:-1] + upper[:-1]


def hull_area(points: Sequence[Point]) -> float:
    hull = convex_hull(points)
    if len(hull) < 3:
        return 0.0
    return polygon_area(hull)
