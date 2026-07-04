from __future__ import annotations

import math
from decimal import Decimal, localcontext
from enum import Enum
from fractions import Fraction
from typing import Protocol, Union, runtime_checkable

Number = Union[float, Decimal, Fraction]


class Precision(str, Enum):
    FLOAT = "float"
    DECIMAL = "decimal"
    EXACT = "exact"


@runtime_checkable
class Backend(Protocol):
    name: str

    @property
    def pi(self): ...

    def sqrt(self, x): ...

    def sin(self, x): ...

    def cos(self, x): ...

    def tan(self, x): ...

    def atan(self, x): ...

    def number(self, x): ...

    def is_finite(self, x) -> bool: ...

    def to_float(self, x) -> float: ...


class FloatBackend:
    name = "float"

    @property
    def pi(self) -> float:
        return math.pi

    def sqrt(self, x):
        return math.sqrt(x)

    def sin(self, x):
        return math.sin(x)

    def cos(self, x):
        return math.cos(x)

    def tan(self, x):
        return math.tan(x)

    def atan(self, x):
        return math.atan(x)

    def number(self, x):
        return float(x)

    def is_finite(self, x) -> bool:
        return math.isfinite(x)

    def to_float(self, x) -> float:
        return float(x)


class DecimalBackend:
    name = "decimal"

    def __init__(self, prec: int = 50) -> None:
        self.prec = prec

    def _mp(self, func_name: str, x):
        import mpmath

        with mpmath.workdps(self.prec + 10):
            value = getattr(mpmath, func_name)(mpmath.mpf(str(x)))
            return Decimal(mpmath.nstr(value, self.prec))

    @property
    def pi(self) -> Decimal:
        import mpmath

        with mpmath.workdps(self.prec + 10):
            return Decimal(mpmath.nstr(mpmath.pi, self.prec))

    def sqrt(self, x) -> Decimal:
        with localcontext() as ctx:
            ctx.prec = self.prec
            return Decimal(str(x)).sqrt()

    def sin(self, x) -> Decimal:
        return self._mp("sin", x)

    def cos(self, x) -> Decimal:
        return self._mp("cos", x)

    def tan(self, x) -> Decimal:
        return self._mp("tan", x)

    def atan(self, x) -> Decimal:
        return self._mp("atan", x)

    def number(self, x) -> Decimal:
        return x if isinstance(x, Decimal) else Decimal(str(x))

    def is_finite(self, x) -> bool:
        return Decimal(str(x)).is_finite()

    def to_float(self, x) -> float:
        return float(x)


class ExactBackend:
    name = "exact"

    @property
    def pi(self):
        import sympy

        return sympy.pi

    def sqrt(self, x):
        import sympy

        return sympy.sqrt(self.number(x))

    def sin(self, x):
        import sympy

        return sympy.sin(self.number(x))

    def cos(self, x):
        import sympy

        return sympy.cos(self.number(x))

    def tan(self, x):
        import sympy

        return sympy.tan(self.number(x))

    def atan(self, x):
        import sympy

        return sympy.atan(self.number(x))

    def number(self, x):
        import sympy

        if isinstance(x, bool):
            return sympy.Integer(int(x))
        if isinstance(x, int):
            return sympy.Integer(x)
        if isinstance(x, Fraction):
            return sympy.Rational(x.numerator, x.denominator)
        if isinstance(x, float):
            return sympy.nsimplify(x, rational=True)
        return sympy.sympify(x)

    def is_finite(self, x) -> bool:
        return bool(getattr(x, "is_finite", True))

    def to_float(self, x) -> float:
        return float(x)


_STRING_BACKENDS = {
    "float": FloatBackend,
    "decimal": DecimalBackend,
    "exact": ExactBackend,
    "symbolic": ExactBackend,
}


def get_backend(spec: str | Precision | Backend = "float") -> Backend:
    if isinstance(spec, Backend):
        return spec
    key = spec.value if isinstance(spec, Precision) else str(spec).strip().lower()
    if key not in _STRING_BACKENDS:
        raise ValueError(f"Unknown backend: {spec}")
    return _STRING_BACKENDS[key]()
