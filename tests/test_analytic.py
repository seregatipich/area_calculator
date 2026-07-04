import math
from unittest import TestCase, main

import sympy

from area_calculator.shapes.circle import Circle
from area_calculator.shapes.circular_regions import (
    Annulus,
    CircularSector,
    CircularSegment,
)
from area_calculator.shapes.ellipse import Ellipse
from area_calculator.shapes.quadrilateral import Quadrilateral, cyclic_polygon_area
from area_calculator.shapes.regular_polygon import RegularPolygon
from area_calculator.shapes.spherical_triangle import SphericalTriangle


class TestEllipse(TestCase):
    def test_area(self):
        self.assertAlmostEqual(Ellipse(2, 1).area(), 2 * math.pi)

    def test_circle_perimeter_limit(self):
        for method in ("ellipe", "agm", "ramanujan"):
            self.assertAlmostEqual(
                Ellipse(3, 3).perimeter(method=method), 2 * math.pi * 3
            )

    def test_known_perimeter(self):
        self.assertAlmostEqual(Ellipse(2, 1).perimeter(), 9.6884482205477, places=9)

    def test_ellipe_agm_agree(self):
        for ratio in (0.1, 0.3, 0.5, 0.9):
            ellipse = Ellipse(1.0, ratio)
            self.assertAlmostEqual(
                ellipse.perimeter(method="ellipe"),
                ellipse.perimeter(method="agm"),
                places=12,
            )

    def test_ramanujan_close(self):
        ellipse = Ellipse(2, 1)
        self.assertAlmostEqual(
            ellipse.perimeter(method="ramanujan"),
            ellipse.perimeter(method="ellipe"),
            places=4,
        )

    def test_axes_normalized(self):
        self.assertEqual(Ellipse(1, 2).area(), Ellipse(2, 1).area())

    def test_exact_area(self):
        self.assertEqual(Ellipse(2, 1, backend="exact").area(), 2 * sympy.pi)

    def test_nonpositive_raises(self):
        with self.assertRaises(ValueError):
            Ellipse(1, 0)


class TestRegularPolygon(TestCase):
    def test_square(self):
        square = RegularPolygon(4, 1)
        self.assertAlmostEqual(square.area(), 1.0)
        self.assertAlmostEqual(square.apothem(), 0.5)
        self.assertAlmostEqual(square.circumradius(), math.sqrt(2) / 2)

    def test_triangle_area(self):
        self.assertAlmostEqual(RegularPolygon(3, 2).area(), math.sqrt(3))

    def test_hexagon_exact(self):
        self.assertEqual(
            RegularPolygon(6, 1, backend="exact").area(), 3 * sympy.sqrt(3) / 2
        )

    def test_from_circumradius_roundtrip(self):
        polygon = RegularPolygon.from_circumradius(5, 3.0)
        self.assertAlmostEqual(polygon.circumradius(), 3.0)

    def test_too_few_sides(self):
        with self.assertRaises(ValueError):
            RegularPolygon(2, 1)

    def test_large_n_approaches_circle(self):
        polygon = RegularPolygon.from_circumradius(100000, 1.0)
        self.assertAlmostEqual(polygon.area(), math.pi, places=4)


class TestQuadrilateral(TestCase):
    def test_cyclic_square(self):
        self.assertAlmostEqual(Quadrilateral.cyclic(1, 1, 1, 1).area(), 1.0)

    def test_brahmagupta(self):
        self.assertAlmostEqual(Quadrilateral.cyclic(3, 4, 5, 6).area(), math.sqrt(360))

    def test_invalid_sides(self):
        with self.assertRaises(ValueError):
            Quadrilateral(1, 1, 1, 10)

    def test_cyclic_polygon_matches_square(self):
        self.assertAlmostEqual(cyclic_polygon_area([1, 1, 1, 1]), 1.0)

    def test_cyclic_polygon_matches_regular_hexagon(self):
        self.assertAlmostEqual(
            cyclic_polygon_area([2.0] * 6), RegularPolygon(6, 2.0).area(), places=6
        )


class TestCircularRegions(TestCase):
    def test_annulus_area(self):
        self.assertAlmostEqual(Annulus(2, 1).area(), 3 * math.pi)

    def test_annulus_matches_circle_difference(self):
        self.assertAlmostEqual(
            Annulus(2, 1).area(), Circle(2).area() - Circle(1).area()
        )

    def test_sector_full_disk(self):
        self.assertAlmostEqual(CircularSector(2, 2 * math.pi).area(), math.pi * 4)

    def test_sector_quarter(self):
        self.assertAlmostEqual(CircularSector(1, math.pi / 2).area(), math.pi / 4)

    def test_segment_semicircle(self):
        self.assertAlmostEqual(CircularSegment(1, math.pi).area(), math.pi / 2)

    def test_segment_small_angle_series(self):
        import mpmath

        radius, theta = 1.0, 1e-4
        with mpmath.workdps(50):
            truth = float(
                mpmath.mpf("0.5")
                * mpmath.mpf(str(radius)) ** 2
                * (mpmath.mpf(str(theta)) - mpmath.sin(mpmath.mpf(str(theta))))
            )
        self.assertLess(abs(CircularSegment(radius, theta).area() - truth), 1e-18)


class TestSphericalTriangle(TestCase):
    def test_octant(self):
        triangle = SphericalTriangle(math.pi / 2, math.pi / 2, math.pi / 2)
        self.assertAlmostEqual(triangle.area(), math.pi / 2)

    def test_from_angles(self):
        triangle = SphericalTriangle.from_angles(math.pi / 2, math.pi / 2, math.pi / 2)
        self.assertAlmostEqual(triangle.spherical_excess(), math.pi / 2)

    def test_radius_scaling(self):
        unit = SphericalTriangle(1.0, 1.0, 1.0)
        scaled = SphericalTriangle(1.0, 1.0, 1.0, radius=3.0)
        self.assertAlmostEqual(scaled.area(), 9.0 * unit.area())

    def test_invalid_arc_raises(self):
        with self.assertRaises(ValueError):
            SphericalTriangle(0.1, 0.1, 3.0)


if __name__ == "__main__":
    main()
