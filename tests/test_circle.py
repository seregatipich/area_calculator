from unittest import TestCase, main

from area_calculator.shapes.circle import Circle


class TestAreaOfCircle(TestCase):
    def test_area(self):
        self.assertAlmostEqual(Circle(1).area(), 3.141592, places=5)
        self.assertEqual(Circle(0).area(), 0)
        self.assertAlmostEqual(Circle(2.5).area(), 19.634954, places=5)

    def test_negative_radius(self):
        with self.assertRaises(
            ValueError
        ):  # Check if area_of_circle raises correct error
            Circle(-1)


if __name__ == "__main__":
    main()
