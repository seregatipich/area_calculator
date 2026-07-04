import math
from fractions import Fraction
from unittest import TestCase, main

import sympy

from area_calculator.analytic.symbolic import (
    as_float,
    exact_circle_area,
    exact_polygon_area,
    exact_triangle_area,
    symbolic_area_under_curve,
    symbolic_matches_numeric,
)
from area_calculator.numerical.integration import area_under_curve
from area_calculator.shapes.circle import Circle
from area_calculator.shapes.triangle import Triangle


class TestExactTriangle(TestCase):
    def test_rational_area(self):
        self.assertEqual(exact_triangle_area(3, 4, 5), Fraction(6))

    def test_irrational_area(self):
        self.assertEqual(exact_triangle_area(7, 7, 7), 49 * sympy.sqrt(3) / 4)

    def test_matches_numeric(self):
        self.assertTrue(
            symbolic_matches_numeric(
                exact_triangle_area(7, 7, 7), Triangle(7, 7, 7).area()
            )
        )

    def test_degenerate_raises(self):
        with self.assertRaises(ValueError):
            exact_triangle_area(1, 1, 10)


class TestExactCircle(TestCase):
    def test_symbolic(self):
        self.assertEqual(exact_circle_area(5), 25 * sympy.pi)

    def test_as_float_matches(self):
        self.assertAlmostEqual(as_float(exact_circle_area(5)), Circle(5).area())


class TestSymbolicIntegration(TestCase):
    def test_quadratic(self):
        x = sympy.Symbol("x")
        self.assertEqual(symbolic_area_under_curve(x**2, x, 0, 1), Fraction(1, 3))

    def test_sine(self):
        x = sympy.Symbol("x")
        self.assertEqual(symbolic_area_under_curve(sympy.sin(x), x, 0, sympy.pi), 2)

    def test_matches_numeric(self):
        x = sympy.Symbol("x")
        exact = symbolic_area_under_curve(sympy.exp(x), x, 0, 1)
        self.assertTrue(
            symbolic_matches_numeric(
                exact, area_under_curve(math.exp, 0, 1)
            )
        )

    def test_no_closed_form_raises(self):
        x = sympy.Symbol("x")
        unknown = sympy.Function("f")(x)
        with self.assertRaises(ValueError):
            symbolic_area_under_curve(unknown, x, 0, 1)

    def test_divergent_raises(self):
        x = sympy.Symbol("x")
        with self.assertRaises(ValueError):
            symbolic_area_under_curve(1 / x, x, 0, 1)


class TestExactPolygon(TestCase):
    def test_unit_square(self):
        square = [
            (Fraction(0), Fraction(0)),
            (Fraction(1), Fraction(0)),
            (Fraction(1), Fraction(1)),
            (Fraction(0), Fraction(1)),
        ]
        self.assertEqual(exact_polygon_area(square), Fraction(1))

    def test_triangle_matches_heron(self):
        triangle = [
            (Fraction(0), Fraction(0)),
            (Fraction(4), Fraction(0)),
            (Fraction(0), Fraction(3)),
        ]
        self.assertEqual(exact_polygon_area(triangle), Fraction(6))
        self.assertEqual(float(exact_polygon_area(triangle)), Triangle(3, 4, 5).area())

    def test_orientation_invariant(self):
        triangle = [
            (Fraction(0), Fraction(0)),
            (Fraction(4), Fraction(0)),
            (Fraction(0), Fraction(3)),
        ]
        self.assertEqual(
            exact_polygon_area(triangle), exact_polygon_area(list(reversed(triangle)))
        )

    def test_float_vertex_raises(self):
        with self.assertRaises(TypeError):
            exact_polygon_area([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])


if __name__ == "__main__":
    main()
