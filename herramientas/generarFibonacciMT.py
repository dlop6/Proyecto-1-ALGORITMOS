#Genera el JSON de la MT de Fibonacci (tabla expandida)

import json, os
from typing import Dict, List


def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b



def main() -> None:
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dirSalida = os.path.join(raiz, "configuracion")
    os.makedirs(dirSalida, exist_ok=True)
    archivoSalida = os.path.join(dirSalida, "fibonacci.json")

    maquina = construirFibonacciMT(maxN=12)
    with open(archivoSalida, "w", encoding="utf-8") as f:
        json.dump(maquina, f, ensure_ascii=False, indent=2)

    print(f"Generado: {archivoSalida}")
    print(f"Estados: {len(maquina['states'])}  |  Transiciones: {len(maquina['transitions'])}")


if __name__ == "__main__":
    main()
