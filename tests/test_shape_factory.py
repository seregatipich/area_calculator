from unittest import TestCase, main

from area_calculator.registry import registered_names
from area_calculator.shape_factory import create_shape
from area_calculator.shapes.circle import Circle
from area_calculator.shapes.shape import Shape
from area_calculator.shapes.triangle import Triangle

FACTORY_ARGS = {
    "circle": (5,),
    "triangle": (3, 4, 5),
    "polygon": ([(0, 0), (1, 0), (1, 1), (0, 1)],),
    "coordinate_triangle": ((0, 0), (4, 0), (0, 3)),
    "ellipse": (2, 1),
    "regular_polygon": (6, 1),
    "quadrilateral": (1, 1, 1, 1),
    "annulus": (2, 1),
    "circular_sector": (1, 1.0),
    "circular_segment": (1, 1.0),
    "spherical_triangle": (1.0, 1.0, 1.0),
    "sphere": (1,),
    "cylinder": (1, 2),
    "cone": (3, 4),
}


class TestFactoryCatalog(TestCase):
    def test_every_registered_name_constructs_a_shape(self):
        for name in registered_names():
            self.assertIn(name, FACTORY_ARGS, f"missing factory args for {name!r}")
            shape = create_shape(name, *FACTORY_ARGS[name])
            self.assertIsInstance(shape, Shape)
            self.assertIsInstance(shape.area(), (int, float))

    def test_create_circle_returns_circle(self):
        self.assertIsInstance(create_shape("circle", 5), Circle)

    def test_create_triangle_returns_triangle(self):
        self.assertIsInstance(create_shape("triangle", 3, 4, 5), Triangle)

    def test_unknown_shape_raises(self):
        with self.assertRaises(ValueError):
            create_shape("dodecahedron", 1)

    def test_case_insensitive_lookup(self):
        self.assertEqual(
            create_shape("CIRCLE", 5).area(), create_shape("circle", 5).area()
        )


if __name__ == "__main__":
    main()
