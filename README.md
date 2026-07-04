# area_calculator

A Python library for computing the area (and related measures) of geometric shapes —
from circles and triangles to polygons, ellipses, solids, and regions defined by curves.

## Features

- Numerically stable triangle area (Kahan's formula, accurate even for needle-thin triangles).
- Precision backends: `float` (default), `decimal`, or `exact` (symbolic, e.g. `4*pi`).
- Registry factory: `create_shape("name", ...)` plus a polymorphic `calculate_area`.
- Coordinate geometry: polygons (shoelace area, centroid, point-in-polygon) and convex hull.
- Analytic shapes: ellipse, regular polygon, quadrilaterals, annulus/sector/segment,
  spherical triangle, and solids (sphere, cylinder, cone).
- Numerical methods: adaptive integration, Green's-theorem area, Monte Carlo, and exact
  symbolic areas via sympy.

## Installation

```bash
pip install git+https://github.com/seregatipich/area_calculator.git
```

Requires `numpy`, `scipy`, and `sympy`.

## Usage

```python
from area_calculator import Circle, Triangle, create_shape, calculate_area, measure

Circle(5).area()                    # 78.53981633974483
Triangle(3, 4, 5).area()            # 6.0
Triangle(3, 4, 5).is_right_angle()  # True

calculate_area(create_shape("triangle", 3, 4, 5))  # 6.0
measure(Circle(1))                  # {"area": 3.14159..., "perimeter": 6.28318...}
```

Exact and arbitrary-precision results:

```python
Circle(2, backend="exact").area()          # 4*pi
Triangle(7, 7, 7, backend="exact").area()  # 49*sqrt(3)/4
Circle(1, backend="decimal").area()        # Decimal("3.14159...")
```

Polygons, solids, and region areas:

```python
import math
from area_calculator import Ellipse, Polygon, Sphere
from area_calculator.numerical import area_under_curve

Ellipse(2, 1).perimeter()                 # 9.6884482205477
Polygon([(0, 0), (4, 0), (0, 3)]).area()  # 6.0
Sphere(2).volume()                        # 33.510321...
area_under_curve(math.sin, 0, math.pi)    # 2.0
```

## Tests

```bash
pip install pytest hypothesis
python -m pytest
```
