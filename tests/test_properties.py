import math
from itertools import permutations
from unittest import TestCase, main

from hypothesis import assume, given
from hypothesis import strategies as st

from area_calculator.geometry.convex_hull import convex_hull, hull_area
from area_calculator.geometry.shoelace import polygon_area
from area_calculator.numerical.heron import kahan_triangle_area
from area_calculator.shapes.circle import Circle
from area_calculator.shapes.triangle import Triangle

coordinate = st.floats(
    min_value=-100, max_value=100, allow_nan=False, allow_infinity=False
)
positive = st.floats(min_value=0.5, max_value=50, allow_nan=False, allow_infinity=False)
point_cloud = st.lists(st.tuples(coordinate, coordinate), min_size=3, max_size=10)


def _valid_triangle(a, b, c_ratio):
    low = abs(a - b)
    high = a + b
    c = low + c_ratio * (high - low)
    return c


class TestShoelaceInvariants(TestCase):
    @given(points=point_cloud, dx=coordinate, dy=coordinate)
    def test_hull_area_translation_invariant(self, points, dx, dy):
        base = hull_area(points)
        assume(base > 1e-3)
        shifted = [(x + dx, y + dy) for x, y in points]
        self.assertTrue(
            math.isclose(hull_area(shifted), base, rel_tol=1e-6, abs_tol=1e-6)
        )

    @given(points=point_cloud, theta=st.floats(0, 2 * math.pi))
    def test_hull_area_rotation_invariant(self, points, theta):
        base = hull_area(points)
        assume(base > 1e-3)
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        rotated = [(x * cos_t - y * sin_t, x * sin_t + y * cos_t) for x, y in points]
        self.assertTrue(
            math.isclose(hull_area(rotated), base, rel_tol=1e-6, abs_tol=1e-6)
        )

    @given(points=point_cloud, k=st.floats(0.1, 10))
    def test_hull_area_scales_quadratically(self, points, k):
        base = hull_area(points)
        assume(base > 1e-3)
        scaled = [(x * k, y * k) for x, y in points]
        self.assertTrue(
            math.isclose(hull_area(scaled), base * k * k, rel_tol=1e-6, abs_tol=1e-6)
        )

    @given(points=point_cloud)
    def test_interior_point_does_not_change_hull_area(self, points):
        hull = convex_hull(points)
        assume(len(hull) >= 3)
        base = polygon_area(hull)
        assume(base > 1e-3)
        center_x = math.fsum(vertex[0] for vertex in hull) / len(hull)
        center_y = math.fsum(vertex[1] for vertex in hull) / len(hull)
        extended = [*points, (center_x, center_y)]
        self.assertTrue(
            math.isclose(hull_area(extended), base, rel_tol=1e-9, abs_tol=1e-9)
        )


class TestTriangleInvariants(TestCase):
    @given(a=positive, b=positive, c_ratio=st.floats(0.02, 0.98), k=st.floats(0.1, 10))
    def test_area_scales_quadratically(self, a, b, c_ratio, k):
        c = _valid_triangle(a, b, c_ratio)
        assume(abs(a - b) + 1e-6 < c < a + b - 1e-6)
        base = Triangle(a, b, c).area()
        assume(base > 1e-6)
        scaled = Triangle(a * k, b * k, c * k).area()
        self.assertTrue(math.isclose(scaled, base * k * k, rel_tol=1e-6))

    @given(a=positive, b=positive, c_ratio=st.floats(0.02, 0.98))
    def test_area_permutation_invariant(self, a, b, c_ratio):
        c = _valid_triangle(a, b, c_ratio)
        assume(abs(a - b) + 1e-6 < c < a + b - 1e-6)
        areas = {kahan_triangle_area(*sides) for sides in permutations((a, b, c))}
        self.assertEqual(len(areas), 1)


class TestCircleInvariants(TestCase):
    @given(r=positive, k=st.floats(0.1, 10))
    def test_area_scales_quadratically(self, r, k):
        self.assertTrue(
            math.isclose(Circle(r * k).area(), Circle(r).area() * k * k, rel_tol=1e-12)
        )


if __name__ == "__main__":
    main()
