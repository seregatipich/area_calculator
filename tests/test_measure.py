import math
from unittest import TestCase, main

from area_calculator.area_calculator import calculate_area, measure
from area_calculator.shapes.circle import Circle
from area_calculator.shapes.solids import Sphere
from area_calculator.shapes.spherical_triangle import SphericalTriangle
from area_calculator.shapes.triangle import Triangle


class TestCalculateArea(TestCase):
    def test_circle(self):
        self.assertEqual(calculate_area(Circle(5)), 78.53981633974483)

    def test_duck_typed_object(self):
        class Blob:
            def area(self):
                return 42.0

        self.assertEqual(calculate_area(Blob()), 42.0)


class TestMeasure(TestCase):
    def test_circle_has_area_and_perimeter(self):
        result = measure(Circle(1))
        self.assertAlmostEqual(result["area"], math.pi)
        self.assertAlmostEqual(result["perimeter"], 2 * math.pi)
        self.assertEqual(set(result), {"area", "perimeter"})

    def test_triangle(self):
        result = measure(Triangle(3, 4, 5))
        self.assertEqual(result["area"], 6.0)
        self.assertEqual(result["perimeter"], 12)

    def test_solid_has_surface_area_and_volume(self):
        result = measure(Sphere(1))
        self.assertAlmostEqual(result["surface_area"], 4 * math.pi)
        self.assertAlmostEqual(result["volume"], 4 / 3 * math.pi)
        self.assertEqual(result["area"], result["surface_area"])

    def test_area_matches_calculate_area(self):
        sphere = Sphere(2)
        self.assertEqual(measure(sphere)["area"], calculate_area(sphere))

    def test_plain_shape_has_area_only(self):
        result = measure(SphericalTriangle(math.pi / 2, math.pi / 2, math.pi / 2))
        self.assertEqual(set(result), {"area"})


if __name__ == "__main__":
    main()
