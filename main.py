from metodo import metodo_biseccion
from time import perf_counter_ns


def main() -> int:
    example = [1, 4, -1, -4]

    init = perf_counter_ns()
    root = metodo_biseccion(example, (0, 2.5), 1e-100)
    end = perf_counter_ns()

    print(f"Raiz: {root}\ntiempo: {end - init} ns")

    return 0


if __name__ == "__main__":
    exit(main())
