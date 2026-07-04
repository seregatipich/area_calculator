import math
from decimal import Decimal
from unittest import TestCase, main

import sympy

from area_calculator.precision.backend import (
    DecimalBackend,
    ExactBackend,
    FloatBackend,
    get_backend,
)
from area_calculator.shapes.circle import Circle
from area_calculator.shapes.shape import Shape, Shape2D, SupportsArea


class TestFloatBackend(TestCase):
    def test_pi(self):
        self.assertEqual(FloatBackend().pi, math.pi)

    def test_sqrt(self):
        self.assertEqual(FloatBackend().sqrt(4), 2.0)


class TestDecimalBackend(TestCase):
    def test_pi_is_decimal_with_precision(self):
        pi = DecimalBackend(prec=30).pi
        self.assertIsInstance(pi, Decimal)
        self.assertTrue(str(pi).startswith("3.14159265358979"))

    def test_sqrt_matches_math(self):
        root = DecimalBackend(prec=30).sqrt(2)
        self.assertIsInstance(root, Decimal)
        self.assertLess(abs(float(root) - math.sqrt(2)), 1e-15)

    def test_global_context_untouched(self):
        from decimal import getcontext

        before = getcontext().prec
        DecimalBackend(prec=30).sqrt(2)
        self.assertEqual(getcontext().prec, before)


class TestExactBackend(TestCase):
    def test_pi_is_symbolic(self):
        self.assertEqual(ExactBackend().pi, sympy.pi)

    def test_sqrt_stays_symbolic(self):
        self.assertEqual(ExactBackend().sqrt(2), sympy.sqrt(2))


class TestGetBackend(TestCase):
    def test_unknown_raises(self):
        with self.assertRaises(ValueError):
            get_backend("quantum")

    def test_passthrough_instance(self):
        backend = FloatBackend()
        self.assertIs(get_backend(backend), backend)


class TestShapeHierarchy(TestCase):
    def test_circle_is_shape2d(self):
        self.assertIsInstance(Circle(1), Shape2D)
        self.assertIsInstance(Circle(1), Shape)

    def test_supports_area_protocol(self):
        self.assertIsInstance(Circle(1), SupportsArea)

    def test_shape_perimeter_default_raises(self):
        class AreaOnly(Shape):
            def area(self):
                return 1.0

        with self.assertRaises(NotImplementedError):
            AreaOnly().perimeter()


class TestCircleBackends(TestCase):
    def test_default_float_golden(self):
        self.assertEqual(Circle(5).area(), 78.53981633974483)

    def test_perimeter(self):
        self.assertAlmostEqual(Circle(1).perimeter(), 2 * math.pi)

    def test_negative_radius_message_preserved(self):
        with self.assertRaisesRegex(ValueError, "Radius can't be negative"):
            Circle(-1)

    def test_exact_backend_area(self):
        self.assertEqual(Circle(2, backend="exact").area(), 4 * sympy.pi)

    def test_exact_float_matches_default(self):
        self.assertAlmostEqual(
            float(Circle(5, backend="exact").area()), Circle(5).area()
        )

    def test_decimal_backend_area(self):
        area = Circle(1, backend="decimal").area()
        self.assertIsInstance(area, Decimal)
        self.assertAlmostEqual(float(area), math.pi)


if __name__ == "__main__":
    main()
