from area_calculator.shapes.shape import Shape


def calculate_area(shape: Shape) -> float:
    return shape.area()

"""
Можно использовать эту функцию не зная тип фигуры в compile-time:

from area_calculator.shape_factory import create_shape
from area_calculator.area_calculator import calculate_area

# Create a Circle and a Triangle dynamically
circle = create_shape("circle", 5)
triangle = create_shape("triangle", 3, 4, 5)

# Calculate areas dynamically
circle_area = calculate_area(circle)
triangle_area = calculate_area(triangle)

print(f"Circle area: {circle_area}")  # Output: Circle area: 78.53981633974483
print(f"Triangle area: {triangle_area}")  # Output: Triangle area: 6.0

"""