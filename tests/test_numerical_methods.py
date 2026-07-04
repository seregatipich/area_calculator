import math
from unittest import TestCase, main

from area_calculator.numerical.greens import parametric_area
from area_calculator.numerical.integration import (
    adaptive_simpson,
    area_between_curves,
    area_under_curve,
)
from area_calculator.numerical.montecarlo import MonteCarloArea, monte_carlo_area


class TestIntegration(TestCase):
    def test_sin_quad(self):
        self.assertAlmostEqual(area_under_curve(math.sin, 0, math.pi), 2.0)

    def test_sin_simpson(self):
        self.assertAlmostEqual(
            area_under_curve(math.sin, 0, math.pi, method="simpson"), 2.0
        )

    def test_quadratic(self):
        self.assertAlmostEqual(area_under_curve(lambda x: x * x, 0, 1), 1 / 3)

    def test_exponential(self):
        self.assertAlmostEqual(area_under_curve(math.exp, 0, 1), math.e - 1)

    def test_reversed_limits(self):
        self.assertAlmostEqual(area_under_curve(math.sin, math.pi, 0), -2.0)

    def test_between_curves(self):
        self.assertAlmostEqual(
            area_between_curves(lambda x: x, lambda x: x * x, 0, 1), 1 / 6
        )

    def test_absolute_between_curves(self):
        signed = area_between_curves(math.sin, lambda x: 0.0, 0, 2 * math.pi)
        absolute = area_between_curves(
            math.sin,
            lambda x: 0.0,
            0,
            2 * math.pi,
            absolute=True,
            breakpoints=(math.pi,),
        )
        self.assertAlmostEqual(signed, 0.0)
        self.assertAlmostEqual(absolute, 4.0)

    def test_equal_limits(self):
        self.assertEqual(area_under_curve(math.sin, 1.0, 1.0), 0.0)

    def test_nonfinite_integrand_raises(self):
        with self.assertRaises(ValueError):
            adaptive_simpson(lambda x: math.inf, 0, 1)

    def test_quad_simpson_agree(self):
        for coefficients in ([1, -2, 3], [0.5, 0, -1, 2]):

            def poly(x, c=coefficients):
                return sum(
                    coefficient * x**power for power, coefficient in enumerate(c)
                )

            self.assertAlmostEqual(
                area_under_curve(poly, -1, 2, method="quad"),
                area_under_curve(poly, -1, 2, method="simpson"),
                places=8,
            )


class TestGreens(TestCase):
    def test_circle(self):
        area = parametric_area(
            lambda t: math.cos(t), lambda t: math.sin(t), 0, 2 * math.pi
        )
        self.assertAlmostEqual(area, math.pi)

    def test_ellipse(self):
        area = parametric_area(
            lambda t: 2 * math.cos(t), lambda t: math.sin(t), 0, 2 * math.pi
        )
        self.assertAlmostEqual(area, 2 * math.pi)

    def test_orientation_signed(self):
        area = parametric_area(
            lambda t: math.cos(-t), lambda t: math.sin(-t), 0, 2 * math.pi, signed=True
        )
        self.assertAlmostEqual(area, -math.pi)

    def test_analytic_derivatives_match(self):
        area = parametric_area(
            math.cos,
            math.sin,
            0,
            2 * math.pi,
            dx_dt=lambda t: -math.sin(t),
            dy_dt=math.cos,
        )
        self.assertAlmostEqual(area, math.pi, places=10)

    def test_open_curve_raises(self):
        with self.assertRaises(ValueError):
            parametric_area(math.cos, math.sin, 0, math.pi)


class TestMonteCarlo(TestCase):
    @staticmethod
    def unit_disk(x, y):
        return x * x + y * y <= 1.0

    def test_disk_estimate(self):
        result = monte_carlo_area(
            self.unit_disk, (-1, 1, -1, 1), n_samples=1_000_000, seed=0
        )
        self.assertIsInstance(result, MonteCarloArea)
        self.assertLess(abs(result.estimate - math.pi), 3 * result.standard_error)
        low, high = result.confidence_interval
        self.assertLess(low, math.pi)
        self.assertGreater(high, math.pi)

    def test_determinism(self):
        first = monte_carlo_area(
            self.unit_disk, (-1, 1, -1, 1), n_samples=50_000, seed=7
        )
        second = monte_carlo_area(
            self.unit_disk, (-1, 1, -1, 1), n_samples=50_000, seed=7
        )
        self.assertEqual(first.estimate, second.estimate)

    def test_zero_area_box_raises(self):
        with self.assertRaises(ValueError):
            monte_carlo_area(self.unit_disk, (0, 0, -1, 1))

    def test_inverted_bounds_raises(self):
        with self.assertRaises(ValueError):
            monte_carlo_area(self.unit_disk, (1, -1, -1, 1))

    def test_wilson_interval_positive_width_when_all_hits(self):
        result = monte_carlo_area(
            lambda x, y: True, (0, 1, 0, 1), n_samples=1000, seed=1
        )
        low, high = result.confidence_interval
        self.assertGreater(high - low, 0.0)


if __name__ == "__main__":
    main()
