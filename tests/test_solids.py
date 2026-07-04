import math
from unittest import TestCase, main

import sympy

from area_calculator.area_calculator import calculate_area
from area_calculator.numerical.pappus import (
    surface_of_revolution_area,
    volume_of_revolution,
)
from area_calculator.shapes.solids import Cone, Cylinder, Sphere


class TestSphere(TestCase):
    def test_surface_area(self):
        self.assertAlmostEqual(Sphere(1).surface_area(), 4 * math.pi)

    def test_volume(self):
        self.assertAlmostEqual(Sphere(1).volume(), 4 / 3 * math.pi)

    def test_calculate_area_is_surface_area(self):
        sphere = Sphere(2)
        self.assertEqual(calculate_area(sphere), sphere.surface_area())

    def test_exact_volume(self):
        self.assertEqual(
            Sphere(1, backend="exact").volume(), sympy.Rational(4, 3) * sympy.pi
        )


class TestCylinder(TestCase):
    def test_surface_area(self):
        self.assertAlmostEqual(Cylinder(1, 2).surface_area(), 6 * math.pi)

    def test_volume(self):
        self.assertAlmostEqual(Cylinder(1, 2).volume(), 2 * math.pi)


class TestCone(TestCase):
    def test_slant_height(self):
        self.assertAlmostEqual(Cone(3, 4).slant_height(), 5.0)

    def test_surface_area(self):
        self.assertAlmostEqual(Cone(3, 4).surface_area(), 24 * math.pi)

    def test_volume(self):
        self.assertAlmostEqual(Cone(3, 4).volume(), 12 * math.pi)


class TestPappus(TestCase):
    def test_torus_volume(self):
        radius, centroid_distance = 1.0, 3.0
        disk_area = math.pi * radius**2
        self.assertAlmostEqual(
            volume_of_revolution(disk_area, centroid_distance),
            2 * math.pi**2 * centroid_distance * radius**2,
        )

    def test_torus_surface(self):
        radius, centroid_distance = 1.0, 3.0
        circle_length = 2 * math.pi * radius
        self.assertAlmostEqual(
            surface_of_revolution_area(circle_length, centroid_distance),
            4 * math.pi**2 * centroid_distance * radius,
        )

    def test_sphere_from_hemisphere(self):
        radius = 2.0
        semicircle_area = math.pi * radius**2 / 2
        centroid_distance = 4 * radius / (3 * math.pi)
        self.assertAlmostEqual(
            volume_of_revolution(semicircle_area, centroid_distance),
            4 / 3 * math.pi * radius**3,
        )

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            volume_of_revolution(-1.0, 2.0)


if __name__ == "__main__":
    main()
