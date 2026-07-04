from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from fractions import Fraction
from typing import Protocol, Union, runtime_checkable

Number = Union[float, Decimal, Fraction]


class Shape(ABC):
    """Abstract base class for geometric shapes."""

    @abstractmethod
    def area(self) -> Number: ...

    def perimeter(self) -> Number:
        raise NotImplementedError(f"{type(self).__name__} does not define a perimeter")


class Shape2D(Shape):
    """A planar shape with both an area and a boundary length."""

    @abstractmethod
    def area(self) -> Number: ...

    @abstractmethod
    def perimeter(self) -> Number: ...


class Solid(Shape):
    """A three-dimensional shape with surface area and volume."""

    @abstractmethod
    def surface_area(self) -> Number: ...

    @abstractmethod
    def volume(self) -> Number: ...

    def area(self) -> Number:
        return self.surface_area()


@runtime_checkable
class SupportsArea(Protocol):
    def area(self) -> Number: ...
