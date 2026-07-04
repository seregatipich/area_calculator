from __future__ import annotations

Point = tuple[float, float]


def orient(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def point_on_segment(p: Point, a: Point, b: Point) -> bool:
    if orient(a, b, p) != 0:
        return False
    within_x = min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
    within_y = min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    return within_x and within_y


def _straddles(d1: float, d2: float) -> bool:
    return (d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    d1 = orient(c, d, a)
    d2 = orient(c, d, b)
    d3 = orient(a, b, c)
    d4 = orient(a, b, d)
    if _straddles(d1, d2) and _straddles(d3, d4):
        return True
    if d1 == 0 and point_on_segment(a, c, d):
        return True
    if d2 == 0 and point_on_segment(b, c, d):
        return True
    if d3 == 0 and point_on_segment(c, a, b):
        return True
    return d4 == 0 and point_on_segment(d, a, b)
