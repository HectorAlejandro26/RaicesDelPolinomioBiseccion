from metodo import metodo_biseccion
from time import perf_counter
import pandas as pd


def main() -> int:
    example = [3, 3, -1]

    init = perf_counter()
    root, aprox, d = metodo_biseccion(
        example,
        interval=(0, 1),
        tol="1e-10",  # 1e-4
        redondeo=8
    )
    end = perf_counter()

    df = pd.DataFrame(d)

    print(
        f"La raiz {"aproximada " if aprox else ""}es: {root}\n" +
        f"tiempo: {end - init} sec\n"
    )

    print(df)

    return 0


if __name__ == "__main__":
    exit(main())
