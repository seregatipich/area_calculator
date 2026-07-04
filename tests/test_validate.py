from unittest import TestCase, main

from area_calculator.precision.validate import validate_radius, validate_triangle_sides
from area_calculator.shapes.circle import Circle
from area_calculator.shapes.triangle import Triangle


class TestValidateTriangle(TestCase):
    def test_valid_passes(self):
        validate_triangle_sides(3, 4, 5)

    def test_negative_message_preserved(self):
        with self.assertRaisesRegex(ValueError, "Triangle's sides cannot be negative"):
            validate_triangle_sides(-1, -2, 0)

    def test_inequality_message_preserved(self):
        with self.assertRaisesRegex(ValueError, "The sides do not form a triangle"):
            validate_triangle_sides(1, 2, 10)

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            validate_triangle_sides(float("nan"), 1, 1)

    def test_inf_rejected(self):
        with self.assertRaises(ValueError):
            validate_triangle_sides(float("inf"), 1, 1)


class TestValidateRadius(TestCase):
    def test_negative_message_preserved(self):
        with self.assertRaisesRegex(ValueError, "Radius can't be negative"):
            validate_radius(-1)

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            validate_radius(float("nan"))


class TestShapeConstructorsValidate(TestCase):
    def test_triangle_nan_rejected(self):
        with self.assertRaises(ValueError):
            Triangle(float("nan"), 1, 1)

    def test_circle_inf_rejected(self):
        with self.assertRaises(ValueError):
            Circle(float("inf"))


if __name__ == "__main__":
    main()
