from typing import Union, Sequence, Tuple, List, Dict, Literal
from re import match
from decimal import Decimal, ROUND_HALF_UP

_Num = Union[Decimal, float, str, Tuple[int, Sequence[int], int]]


def __eval_func(coefs: Sequence[Decimal], value: Decimal) -> Decimal:
    res = coefs[-1]

    for i in range(len(coefs) - 1):
        exp = len(coefs) - i - 1
        res += coefs[i] * (value ** exp)
    return res


_assertions: bool = True
"""Default: True"""
_l_s: str = "1"
"""Default: 1.0"""
_l_i: str = "1e-1000"
"""Default: 1e-1000"""


def metodo_biseccion(
    coefs: Sequence[_Num],
    interval: Tuple[_Num, _Num] = (0.0, 1.0),
    tol: _Num = "1e-6",
    redondeo: int = 8
) -> Tuple[float, bool, Dict[str, List[Decimal]]]:
    if _assertions:
        assert len(interval) == 2, "Formato de intervalo no valido."
        assert interval[0] < interval[1], "El primer valor debe se menor que el segundo."
        tol: Decimal = Decimal(str(tol))
        assert Decimal(_l_i) <= tol < Decimal(_l_s), \
            f"La tolerancia debe ser mayor que {_l_i} y menor que {_l_s}"
        assert match(r"^(?:0.0*1|\d[eE]\-[1234567890]{1,3}0?)$", str(tol)), \
            f"Solo son validos numeros 1e-N, siempre mayor que {_l_i} y menor que {_l_s}."

    data: Dict[Literal["a", "b", "f(a)", "f(b)", "c", "f(c)"], List[Decimal]] = {
        "a": [],
        "b": [],
        "f(a)": [],
        "f(b)": [],
        "c": [],
        "f(c)": [],
    }

    coefs: List[Decimal] = list(map(Decimal, coefs))
    a, b = tuple(map(Decimal, interval))
    c = (a + b) / 2
    fc = __eval_func(coefs, c)

    _iteraciones = 0
    while abs(fc) > tol:
        fa = __eval_func(coefs, a)
        fb = __eval_func(coefs, b)
        fc = __eval_func(coefs, c)

        def format_decimal(x: Decimal) -> Decimal:
            return x.quantize(Decimal("0."+"0"*(redondeo-1)+"1"), ROUND_HALF_UP)

        data["a"].append(format_decimal(a))
        data["f(a)"].append(format_decimal(fa))
        data["b"].append(format_decimal(b))
        data["f(b)"].append(format_decimal(fb))
        data["c"].append(format_decimal(c))
        data["f(c)"].append(format_decimal(fc))

        _iteraciones += 1

        if fa == 0 or fb == 0 or fc == 0:
            print(f"No. De iteraciones: {_iteraciones}")
            return (
                float(a if fa == 0 else b if fb == 0 else c),
                False,
                data
            )

        elif fa * fc < 0:
            b = c

        elif fb * fc < 0:
            a = c

        else:
            raise ArithmeticError(
                "No se encuentró ninguna raiz dentro del intervalo")

        c = (a + b) / 2

    else:
        print(f"No. De iteraciones: {_iteraciones}")
        return float(c), True, data
