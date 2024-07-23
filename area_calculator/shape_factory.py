from area_calculator.shapes.circle import Circle
from area_calculator.shapes.triangle import Triangle


def create_shape(shape_type, *args):
    if shape_type == "circle":
        return Circle(*args)
    elif shape_type == "triangle":
        return Triangle(*args)
    else:
        raise ValueError(f"Unknown shape type: {shape_type}")
