from typing import Any

import area_calculator.shapes  # noqa: F401  (ensures every shape registers on import)
from area_calculator.registry import resolve
from area_calculator.shapes.shape import Shape


def create_shape(shape_type: str, *args: Any) -> Shape:
    return resolve(shape_type)(*args)
