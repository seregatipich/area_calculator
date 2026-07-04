import math
from decimal import Decimal
from itertools import permutations
from unittest import TestCase, main

import mpmath
import sympy

from area_calculator.numerical.heron import kahan_triangle_area, triangle_area
from area_calculator.precision.backend import Precision
from area_calculator.shapes.triangle import Triangle


def naive_heron(a, b, c):
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def mp_area(a, b, c, dps=60):
    with mpmath.workdps(dps):
        sides = sorted((mpmath.mpf(a), mpmath.mpf(b), mpmath.mpf(c)), reverse=True)
        x, y, z = sides
        product = (x + (y + z)) * (z - (x - y)) * (z + (x - y)) * (x + (y - z))
        return float(mpmath.sqrt(product) / 4)


class TestKahanKnownValues(TestCase):
    def test_right_triangle(self):
        self.assertEqual(kahan_triangle_area(3, 4, 5), 6.0)

    def test_equilateral(self):
        self.assertAlmostEqual(kahan_triangle_area(10, 10, 10), 43.30127, places=5)

    def test_five_twelve_thirteen(self):
        self.assertEqual(kahan_triangle_area(5, 12, 13), 30.0)

    def test_permutation_invariance(self):
        areas = {kahan_triangle_area(*sides) for sides in permutations((3, 4, 5))}
        self.assertEqual(len(areas), 1)

    def test_degenerate_raises(self):
        with self.assertRaises(ValueError):
            kahan_triangle_area(1, 1, 10)


class TestKahanNeedleRegression(TestCase):
    def test_kahan_beats_naive_on_needle(self):
        a, b, c = 100000.0, 99999.99979, 0.00029
        truth = mp_area(a, b, c)
        kahan = kahan_triangle_area(a, b, c)
        naive = naive_heron(a, b, c)
        self.assertLess(abs(kahan - truth) / truth, 1e-12)
        self.assertGreater(abs(naive - truth) / truth, 1e-9)


class TestTriangleAreaBackends(TestCase):
    def test_decimal_precision(self):
        area = triangle_area(7, 7, 7, Precision.DECIMAL)
        self.assertIsInstance(area, Decimal)
        self.assertLess(abs(float(area) - kahan_triangle_area(7, 7, 7)), 1e-9)

    def test_exact_rational_area(self):
        self.assertEqual(triangle_area(3, 4, 5, Precision.EXACT), sympy.Integer(6))

    def test_exact_irrational_area(self):
        self.assertEqual(
            triangle_area(7, 7, 7, Precision.EXACT), 49 * sympy.sqrt(3) / 4
        )


class TestTriangleShapeIntegration(TestCase):
    def test_area_matches_kahan(self):
        self.assertEqual(Triangle(3, 4, 5).area(), 6.0)

    def test_perimeter(self):
        self.assertEqual(Triangle(3, 4, 5).perimeter(), 12)

    def test_is_right_angle_preserved(self):
        self.assertTrue(Triangle(3, 4, 5).is_right_angle())
        self.assertFalse(Triangle(3, 3, 3).is_right_angle())

    def test_exact_backend(self):
        self.assertEqual(
            Triangle(7, 7, 7, backend="exact").area(), 49 * sympy.sqrt(3) / 4
        )


if __name__ == "__main__":
    main()
