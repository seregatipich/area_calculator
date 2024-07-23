from unittest import TestCase, main

from area_calculator.area_calculator import calculate_area
from area_calculator.shape_factory import create_shape


class TestAreaCalculator(TestCase):
    def test_calculate_circle_area(self):
        circle = create_shape("circle", 5)
        self.assertAlmostEqual(calculate_area(circle), 78.53981633974483, places=6)

    def test_calculate_triangle_area(self):
        triangle = create_shape("triangle", 3, 4, 5)
        self.assertAlmostEqual(calculate_area(triangle), 6.0, places=6)


if __name__ == "__main__":
    main()
