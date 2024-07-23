from unittest import TestCase, main

from area_calculator.shapes.triangle import Triangle


class TestAreaOfTriangle(TestCase):
    def test_area(self):
        self.assertAlmostEqual(Triangle(3, 4, 5).area(), 6.0, places=6)
        self.assertAlmostEqual(Triangle(10, 10, 10).area(), 43.30127, places=5)

    def test_invalid_sides(self):
        with self.assertRaises(ValueError):
            Triangle(1, 2, 10)

    def test_negative_sides(self):
        with self.assertRaises(ValueError):
            Triangle(-1, -2, 0)


if __name__ == "__main__":
    main()
