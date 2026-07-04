from __future__ import annotations

from collections.abc import Sequence
from math import hypot

from area_calculator.geometry.predicates import Point, orient
from area_calculator.geometry.shoelace import (
    centroid,
    contains_point,
    orientation,
    perimeter,
    polygon_area,
    signed_area,
)
from area_calculator.registry import register

from .shape import Shape2D


@register("polygon")
class Polygon(Shape2D):
    """Simple polygon defined by an ordered sequence of vertices."""

    def __init__(self, vertices: Sequence[Point]):
        points = [tuple(vertex) for vertex in vertices]
        if len(points) >= 2 and points[0] == points[-1]:
            points = points[:-1]
        if len(points) < 3:
            raise ValueError("A polygon needs at least three vertices")
        self.vertices = points

    def signed_area(self) -> float:
        return signed_area(self.vertices)

    def area(self) -> float:
        return polygon_area(self.vertices)

    def perimeter(self) -> float:
        return perimeter(self.vertices)

    def centroid(self) -> Point:
        return centroid(self.vertices)

    def orientation(self) -> str:
        return orientation(self.vertices)

    def contains_point(self, point: Point, **kwargs) -> bool:
        return contains_point(self.vertices, point, **kwargs)


@register("coordinate_triangle")
class CoordinateTriangle(Shape2D):
    """Triangle defined by three coordinates; area from the cross product."""

    def __init__(self, a: Point, b: Point, c: Point):
        self.a = tuple(a)
        self.b = tuple(b)
        self.c = tuple(c)
        if orient(self.a, self.b, self.c) == 0:
            raise ValueError("The points are collinear")

    def signed_area(self) -> float:
        return 0.5 * orient(self.a, self.b, self.c)

    def area(self) -> float:
        return abs(self.signed_area())

    def side_lengths(self) -> tuple[float, float, float]:
        length_a = hypot(self.b[0] - self.c[0], self.b[1] - self.c[1])
        length_b = hypot(self.c[0] - self.a[0], self.c[1] - self.a[1])
        length_c = hypot(self.a[0] - self.b[0], self.a[1] - self.b[1])
        return length_a, length_b, length_c

    def perimeter(self) -> float:
        return sum(self.side_lengths())

    def centroid(self) -> Point:
        x = (self.a[0] + self.b[0] + self.c[0]) / 3
        y = (self.a[1] + self.b[1] + self.c[1]) / 3
        return (x, y)

    def incenter(self) -> Point:
        length_a, length_b, length_c = self.side_lengths()
        total = length_a + length_b + length_c
        x = (length_a * self.a[0] + length_b * self.b[0] + length_c * self.c[0]) / total
        y = (length_a * self.a[1] + length_b * self.b[1] + length_c * self.c[1]) / total
        return (x, y)

    def circumcenter(self) -> Point:
        ax, ay = self.a
        bx, by = self.b
        cx, cy = self.c
        denominator = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        a_sq = ax * ax + ay * ay
        b_sq = bx * bx + by * by
        c_sq = cx * cx + cy * cy
        ux = (a_sq * (by - cy) + b_sq * (cy - ay) + c_sq * (ay - by)) / denominator
        uy = (a_sq * (cx - bx) + b_sq * (ax - cx) + c_sq * (bx - ax)) / denominator
        return (ux, uy)

    def inradius(self) -> float:
        semi_perimeter = self.perimeter() / 2
        return self.area() / semi_perimeter

    def circumradius(self) -> float:
        length_a, length_b, length_c = self.side_lengths()
        return length_a * length_b * length_c / (4 * self.area())
