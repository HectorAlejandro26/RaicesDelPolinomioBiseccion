from typing import Union, Sequence, Tuple
from re import match
from decimal import Decimal

_Num = Union[Decimal, float, str, Tuple[int, Sequence[int], int]]


def __eval_func(coefs: Sequence[Decimal], value: Decimal) -> Decimal:
    res = coefs[-1]

    for i in range(len(coefs) - 1):
        exp = len(coefs) - i - 1
        res += coefs[i] * (value ** exp)
    return res


_assertions: bool = True
"""Default: True"""
_l_s: Decimal = Decimal(1.0)
"""Default: 1.0"""
_l_i: Decimal = Decimal(1e-1000)
"""Default: 1e-1000"""


def metodo_biseccion(
    coefs: Sequence[_Num],
    interval: Tuple[_Num, _Num] = (0.0, 0.1),
    tol: _Num = "1e-6"
) -> float:
    if _assertions:
        assert len(interval) == 2, "Formato de intervalo no valido."
        assert interval[0] < interval[1], "El primer valor debe se menor que el segundo."
        tol: Decimal = Decimal(str(tol))
        assert _l_i <= tol < _l_s, \
            f"La tolerancia debe ser mayor que {_l_i} y menor que {_l_s}"
        assert match(r"^(?:0.0*1|\d[eE]\-[1234567890]{1,3}0?)$", str(tol)), \
            f"Solo son validos numeros 1e-N, siempre mayor que {_l_i} y menor que {_l_s}."

    a, b = tuple(map(Decimal, interval))
    c = (a + b) / 2

    while abs(b - a) >= tol:
        fa = __eval_func(coefs, a)
        fb = __eval_func(coefs, b)
        fc = __eval_func(coefs, c)

        if fa == 0 or fb == 0 or fc == 0:
            return float(a if fa == 0 else b if fb == 0 else c)

        elif fa * fc < 0:
            b = c

        elif fb * fc < 0:
            a = c

        else:
            raise ArithmeticError(
                "No se encuentró ninguna raiz dentro del intervalo")

        c = (a + b) / 2

    else:
        print("Se obtuvo una aproximacion")
        return float(c)
