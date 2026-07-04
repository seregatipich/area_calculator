from unittest import TestCase, main

from area_calculator.registry import register, registered_names, resolve
from area_calculator.shape_factory import create_shape
from area_calculator.shapes.circle import Circle
from area_calculator.shapes.triangle import Triangle


class TestRegistry(TestCase):
    def test_resolve_returns_registered_class(self):
        self.assertIs(resolve("circle"), Circle)
        self.assertIs(resolve("triangle"), Triangle)

    def test_resolve_is_case_insensitive(self):
        self.assertIs(resolve("CIRCLE"), Circle)
        self.assertIs(resolve("  Triangle  "), Triangle)

    def test_resolve_unknown_raises(self):
        with self.assertRaises(ValueError):
            resolve("hexagon")

    def test_registered_names_includes_builtins(self):
        names = registered_names()
        self.assertIn("circle", names)
        self.assertIn("triangle", names)

    def test_duplicate_registration_raises(self):
        with self.assertRaises(ValueError):

            @register("circle")
            class DuplicateCircle:
                pass


class TestFactoryUsesRegistry(TestCase):
    def test_create_circle(self):
        self.assertIsInstance(create_shape("circle", 5), Circle)

    def test_create_triangle(self):
        self.assertIsInstance(create_shape("triangle", 3, 4, 5), Triangle)

    def test_unknown_shape_raises(self):
        with self.assertRaises(ValueError):
            create_shape("hexagon", 1)

    def test_unknown_shape_message_preserved(self):
        with self.assertRaisesRegex(ValueError, "Unknown shape type: hexagon"):
            create_shape("hexagon", 1)


if __name__ == "__main__":
    main()
