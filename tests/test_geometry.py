from unittest import TestCase, main

from scipy.spatial import ConvexHull

from area_calculator.geometry.convex_hull import convex_hull, hull_area
from area_calculator.geometry.predicates import orient, point_on_segment
from area_calculator.geometry.shoelace import (
    centroid,
    contains_point,
    orientation,
    perimeter,
    polygon_area,
    signed_area,
)
from area_calculator.geometry.validity import is_simple_polygon
from area_calculator.shape_factory import create_shape
from area_calculator.shapes.polygon import CoordinateTriangle, Polygon
from area_calculator.shapes.triangle import Triangle

UNIT_SQUARE = [(0, 0), (1, 0), (1, 1), (0, 1)]
RIGHT_TRIANGLE = [(0, 0), (4, 0), (0, 3)]


class TestPredicates(TestCase):
    def test_orient_ccw_positive(self):
        self.assertGreater(orient((0, 0), (1, 0), (0, 1)), 0)

    def test_orient_cw_negative(self):
        self.assertLess(orient((0, 0), (0, 1), (1, 0)), 0)

    def test_point_on_segment(self):
        self.assertTrue(point_on_segment((0.5, 0), (0, 0), (1, 0)))
        self.assertFalse(point_on_segment((0.5, 0.5), (0, 0), (1, 0)))


class TestShoelace(TestCase):
    def test_unit_square_area(self):
        self.assertEqual(polygon_area(UNIT_SQUARE), 1.0)

    def test_signed_area_orientation(self):
        self.assertGreater(signed_area(UNIT_SQUARE), 0)
        self.assertLess(signed_area(list(reversed(UNIT_SQUARE))), 0)

    def test_orientation_labels(self):
        self.assertEqual(orientation(UNIT_SQUARE), "CCW")
        self.assertEqual(orientation(list(reversed(UNIT_SQUARE))), "CW")

    def test_triangle_matches_heron(self):
        self.assertAlmostEqual(polygon_area(RIGHT_TRIANGLE), Triangle(3, 4, 5).area())

    def test_translation_invariance(self):
        shifted = [(x + 1e6, y + 1e6) for x, y in UNIT_SQUARE]
        self.assertAlmostEqual(polygon_area(shifted), 1.0)

    def test_centroid_and_perimeter(self):
        cx, cy = centroid(UNIT_SQUARE)
        self.assertAlmostEqual(cx, 0.5)
        self.assertAlmostEqual(cy, 0.5)
        self.assertAlmostEqual(perimeter(UNIT_SQUARE), 4.0)

    def test_too_few_vertices(self):
        with self.assertRaises(ValueError):
            polygon_area([(0, 0), (1, 1)])


class TestContainsPoint(TestCase):
    def test_inside(self):
        self.assertTrue(contains_point(UNIT_SQUARE, (0.5, 0.5)))

    def test_outside(self):
        self.assertFalse(contains_point(UNIT_SQUARE, (2, 2)))

    def test_boundary_toggle(self):
        self.assertTrue(contains_point(UNIT_SQUARE, (0.5, 0), include_boundary=True))
        self.assertFalse(contains_point(UNIT_SQUARE, (0.5, 0), include_boundary=False))

    def test_winding_and_ray_agree(self):
        concave = [(0, 0), (4, 0), (4, 4), (2, 1), (0, 4)]
        for point in [(2, 0.5), (2, 3), (1, 1), (3, 3)]:
            self.assertEqual(
                contains_point(concave, point, method="winding"),
                contains_point(concave, point, method="ray"),
            )


class TestConvexHull(TestCase):
    def test_hull_excludes_interior(self):
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
        hull = convex_hull(points)
        self.assertEqual(len(hull), 4)
        self.assertNotIn((0.5, 0.5), hull)

    def test_hull_area(self):
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
        self.assertAlmostEqual(hull_area(points), 1.0)

    def test_matches_scipy(self):
        points = [(0, 0), (2, 0), (2, 3), (1, 5), (0, 3), (1, 1)]
        self.assertAlmostEqual(hull_area(points), ConvexHull(points).volume)

    def test_collinear_degenerate(self):
        self.assertEqual(hull_area([(0, 0), (1, 1), (2, 2)]), 0.0)


class TestValidity(TestCase):
    def test_square_is_simple(self):
        self.assertTrue(is_simple_polygon(UNIT_SQUARE))

    def test_bowtie_not_simple(self):
        self.assertFalse(is_simple_polygon([(0, 0), (1, 1), (1, 0), (0, 1)]))


class TestCoordinateTriangle(TestCase):
    def test_area(self):
        self.assertAlmostEqual(CoordinateTriangle((0, 0), (4, 0), (0, 3)).area(), 6.0)

    def test_centroid(self):
        cx, cy = CoordinateTriangle((0, 0), (4, 0), (0, 3)).centroid()
        self.assertAlmostEqual(cx, 4 / 3)
        self.assertAlmostEqual(cy, 1.0)

    def test_inradius(self):
        self.assertAlmostEqual(
            CoordinateTriangle((0, 0), (4, 0), (0, 3)).inradius(), 1.0
        )

    def test_circumradius(self):
        self.assertAlmostEqual(
            CoordinateTriangle((0, 0), (4, 0), (0, 3)).circumradius(), 2.5
        )

    def test_circumcenter(self):
        ux, uy = CoordinateTriangle((0, 0), (4, 0), (0, 3)).circumcenter()
        self.assertAlmostEqual(ux, 2.0)
        self.assertAlmostEqual(uy, 1.5)

    def test_collinear_raises(self):
        with self.assertRaises(ValueError):
            CoordinateTriangle((0, 0), (1, 1), (2, 2))


class TestPolygonShape(TestCase):
    def test_area(self):
        self.assertEqual(Polygon(UNIT_SQUARE).area(), 1.0)

    def test_factory(self):
        polygon = create_shape("polygon", UNIT_SQUARE)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(polygon.area(), 1.0)

    def test_closing_vertex_stripped(self):
        closed = [*UNIT_SQUARE, (0, 0)]
        self.assertEqual(Polygon(closed).area(), 1.0)


if __name__ == "__main__":
    main()
