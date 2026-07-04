from unittest import TestCase, main

from area_calculator.precision.error import AreaEstimate, triangle_area_with_error
from area_calculator.shapes.triangle import Triangle


class TestAreaWithError(TestCase):
    def test_well_conditioned_small_bound(self):
        estimate = triangle_area_with_error(3, 4, 5)
        self.assertIsInstance(estimate, AreaEstimate)
        self.assertEqual(estimate.value, 6.0)
        self.assertLess(estimate.condition_number, 100)
        self.assertLess(estimate.relative_error_bound, 1e-12)

    def test_needle_reports_large_condition_number(self):
        estimate = triangle_area_with_error(100000.0, 99999.99979, 0.00029)
        self.assertGreater(estimate.condition_number, 1e6)

    def test_bound_brackets_true_error(self):
        import mpmath

        a, b, c = 100000.0, 99999.99979, 0.00029
        with mpmath.workdps(60):
            sides = sorted((mpmath.mpf(a), mpmath.mpf(b), mpmath.mpf(c)), reverse=True)
            x, y, z = sides
            product = (x + (y + z)) * (z - (x - y)) * (z + (x - y)) * (x + (y - z))
            truth = float(mpmath.sqrt(product) / 4)
        estimate = triangle_area_with_error(a, b, c)
        self.assertLessEqual(abs(estimate.value - truth), estimate.absolute_error_bound)

    def test_triangle_method(self):
        estimate = Triangle(3, 4, 5).area_with_error()
        self.assertEqual(estimate.value, 6.0)


if __name__ == "__main__":
    main()
