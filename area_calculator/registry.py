from __future__ import annotations

from typing import Callable, TypeVar

_SHAPE_REGISTRY: dict[str, type] = {}

ShapeT = TypeVar("ShapeT")


def register(name: str) -> Callable[[type[ShapeT]], type[ShapeT]]:
    key = name.strip().lower()

    def decorator(shape_cls: type[ShapeT]) -> type[ShapeT]:
        if key in _SHAPE_REGISTRY:
            raise ValueError(f"Shape type already registered: {key}")
        _SHAPE_REGISTRY[key] = shape_cls
        return shape_cls

    return decorator


def resolve(shape_type: str) -> type:
    key = shape_type.strip().lower()
    if key not in _SHAPE_REGISTRY:
        raise ValueError(f"Unknown shape type: {shape_type}")
    return _SHAPE_REGISTRY[key]


def registered_names() -> tuple[str, ...]:
    return tuple(sorted(_SHAPE_REGISTRY))
