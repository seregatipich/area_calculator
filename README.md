# area_calculator

`area_calculator` is a Python library for calculating the area of various geometric shapes. This library is created as the first task from a test assignment for the Python trainee vacancy at Mindbox. 

## Installation

Install the library using pip:

```bash
pip install geometry_calculator
```

## Usage

### Calculate the Area of a Circle

Calculate area of a circle based on a given radius:

```Python
from geometry_calculator import Circle

# Create a Circle object with radius 5
circle = Circle(5)

print(circle.area())  # Output: 78.53981633974483
```

### Calculate the Area of a Triangle

Calculate area of a triangle based on the given sides:

```Python
from geometry_calculator import Triangle

# Create a Triangle object with sides 3, 4, 5
triangle = Triangle(3, 4, 5)

print(triangle.area())  # Output: 6.0
```

### Adding New Shapes

To add a new shape, create a new class that inherits from Shape and implement area method and update '__init__' files.

Example: 'area_calculator/shapes/square.py'
```Python
from geometry_calculator.shapes.shape import Shape

class Square(Shape):
    def __init__(self, side):
        if side < 0:
            raise ValueError("Side length cannot be negative")
        self.side = side
    
    def area(self):
        return self.side ** 2
```

Example: 'area_calculator/shapes/__init__.py'
```Python
from .circle import Circle
from .triangle import Triangle
from .square import Square


__all__ = ["Circle", "Triangle", "Square"]
```

Example: 'area_calculator/__init__.py'
```Python
from .shapes.circle import Circle
from .shapes.triangle import Triangle
from .shapes.square import Square


__all__ = ["Circle", "Triangle", "Square"]
```