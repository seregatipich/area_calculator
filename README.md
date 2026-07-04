# area_calculator

`area_calculator` is a Python library for computing the area (and related
measures) of geometric shapes. It began as a Mindbox trainee test assignment —
circle and triangle areas, an extensible design, type-agnostic dispatch, and a
right-triangle check — and has grown into a small but mathematically serious
geometry toolkit: numerically-stable formulas, coordinate geometry, analytic and
solid shapes, numerical integration, Monte Carlo estimation, and exact/symbolic
results.

## Highlights

- **Numerically-stable triangle area.** `Triangle.area()` uses Kahan's
  cancellation-free reformulation of Heron's formula, which stays accurate for
  needle-thin triangles where naive Heron loses ~8 significant digits.
- **Pluggable precision backends.** Every core shape accepts `backend="float"`
  (default, fast), `"decimal"` (arbitrary precision), or `"exact"` (symbolic,
  closed-form results like `4*pi` or `49*sqrt(3)/4`).
- **Auto-registering factory.** New shapes register themselves with a
  `@register("name")` decorator; `create_shape("name", ...)` needs no edits.
- **Computational geometry.** Polygons from vertices (shoelace signed area,
  centroid, point-in-polygon), Andrew's monotone-chain convex hull, coordinate
  triangles with incenter/circumcenter/radii, simple-polygon detection.
- **Analytic shapes.** Ellipse (elliptic-integral perimeter), regular polygons,
  Bretschneider/Brahmagupta quadrilaterals, annulus/sector/segment, spherical
  triangles (L'Huilier), and 3D solids (sphere, cylinder, cone).
- **Numerical & exact methods.** Adaptive integration (area under/between
  curves), Green's-theorem area of a parametric curve, seeded Monte Carlo with a
  Wilson confidence interval, and a `sympy`-backed exact/symbolic module.

## Installation

```bash
pip install git+https://github.com/seregatipich/area_calculator.git
```

Runtime dependencies: `numpy`, `scipy`, `sympy` (used lazily — the pure-stdlib
paths import none of them).

## Basic usage

```python
from area_calculator import Circle, Triangle, calculate_area, create_shape

Circle(5).area()          # 78.53981633974483
Triangle(3, 4, 5).area()  # 6.0
Triangle(3, 4, 5).is_right_angle()  # True

# Type-agnostic dispatch (shape type unknown at compile time)
shape = create_shape("triangle", 3, 4, 5)
calculate_area(shape)     # 6.0
```

`measure(shape)` returns every relevant quantity at once:

```python
from area_calculator import measure

measure(Circle(1))    # {"area": 3.14159..., "perimeter": 6.28318...}
measure(Sphere(1))    # {"area": ..., "surface_area": ..., "volume": ...}
```

## Precision backends

```python
import sympy
from area_calculator import Circle, Triangle

Circle(2, backend="exact").area()          # 4*pi  (a sympy expression)
Triangle(7, 7, 7, backend="exact").area()  # 49*sqrt(3)/4
Circle(1, backend="decimal").area()        # Decimal("3.14159265358979...")
```

The default `float` backend reproduces the classic results bit-for-bit.

## Shape catalog

| Category | Shapes (factory name) |
|----------|-----------------------|
| Basic | `circle`, `triangle` |
| Coordinate | `polygon`, `coordinate_triangle` |
| Analytic 2D | `ellipse`, `regular_polygon`, `quadrilateral`, `annulus`, `circular_sector`, `circular_segment`, `spherical_triangle` |
| Solids | `sphere`, `cylinder`, `cone` |

```python
from area_calculator import Ellipse, RegularPolygon, Polygon, Sphere

Ellipse(2, 1).area()                 # 2*pi
Ellipse(2, 1).perimeter()            # 9.6884482205477 (via elliptic integral)
RegularPolygon(6, 1).area()          # 2.598076...
Polygon([(0, 0), (4, 0), (0, 3)]).area()   # 6.0
Sphere(2).volume()                   # 33.510321...
```

## Computational geometry

```python
from area_calculator.geometry import convex_hull, hull_area, is_simple_polygon
from area_calculator.shapes.polygon import CoordinateTriangle

hull_area([(0, 0), (2, 0), (2, 3), (1, 5), (1, 1)])   # area of the convex hull
is_simple_polygon([(0, 0), (1, 1), (1, 0), (0, 1)])   # False (a bow-tie)

triangle = CoordinateTriangle((0, 0), (4, 0), (0, 3))
triangle.circumradius()   # 2.5
triangle.incenter()       # (1.0, 1.0)
```

## Numerical & exact methods

```python
import math
from area_calculator.numerical import area_under_curve, parametric_area, monte_carlo_area
from area_calculator.analytic.symbolic import exact_triangle_area, symbolic_area_under_curve
import sympy

area_under_curve(math.sin, 0, math.pi)                       # 2.0
parametric_area(math.cos, math.sin, 0, 2 * math.pi)          # pi (Green's theorem)
monte_carlo_area(lambda x, y: x * x + y * y <= 1,
                 (-1, 1, -1, 1), n_samples=1_000_000, seed=0).estimate  # ~pi

exact_triangle_area(3, 4, 5)                                 # Fraction(6, 1)
x = sympy.Symbol("x")
symbolic_area_under_curve(x**2, x, 0, 1)                     # 1/3 (exact)
```

## Adding a new shape

Subclass `Shape2D` (or `Solid`), implement the required methods, and decorate the
class with `@register("name")` so the factory can find it. Then import the module
from `area_calculator/shapes/__init__.py` so registration runs on import.

```python
# area_calculator/shapes/square.py
from area_calculator.registry import register

from .shape import Shape2D


@register("square")
class Square(Shape2D):
    def __init__(self, side):
        if side < 0:
            raise ValueError("Side length cannot be negative")
        self.side = side

    def area(self):
        return self.side**2

    def perimeter(self):
        return 4 * self.side
```

No changes to the factory are needed — `create_shape("square", 2)` works once the
module is imported.

## Development

```bash
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
python -m pytest        # run the test suite
ruff check . && ruff format --check .
```
