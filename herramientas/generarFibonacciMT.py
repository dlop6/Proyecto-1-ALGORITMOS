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


def construirFibonacciMT(maxN: int = 12) -> Dict:
    """Genera la definición completa de la MT que calcula F(n) en unario."""
    estados: List[str] = ["q0", "q_aceptar", "q_overflow"]
    transiciones: List[Dict[str, str]] = []

    for i in range(1, maxN + 1):
        estados.append(f"q{i}")

    for i in range(0, maxN + 1):
        fn = fibonacci(i)
        if fn >= 2:
            for k in range(1, fn + 1):
                estados.append(f"q_out_{i}_{k}")

    transiciones.append({"current_state": "q0", "read_symbol": "B",
                         "next_state": "q_aceptar", "write_symbol": "B", "move": "N"})
    transiciones.append({"current_state": "q0", "read_symbol": "1",
                         "next_state": "q1", "write_symbol": "B", "move": "R"})

    for i in range(1, maxN):
        transiciones.append({"current_state": f"q{i}", "read_symbol": "1",
                             "next_state": f"q{i+1}", "write_symbol": "B", "move": "R"})

    transiciones.append({"current_state": f"q{maxN}", "read_symbol": "1",
                         "next_state": "q_overflow", "write_symbol": "B", "move": "R"})

    for i in range(1, maxN + 1):
        fn = fibonacci(i)
        if fn == 0:
            transiciones.append({"current_state": f"q{i}", "read_symbol": "B",
                                 "next_state": "q_aceptar", "write_symbol": "B", "move": "N"})
        elif fn == 1:
            transiciones.append({"current_state": f"q{i}", "read_symbol": "B",
                                 "next_state": "q_aceptar", "write_symbol": "1", "move": "N"})
        else:
            transiciones.append({"current_state": f"q{i}", "read_symbol": "B",
                                 "next_state": f"q_out_{i}_1", "write_symbol": "B", "move": "N"})

    for i in range(1, maxN + 1):
        fn = fibonacci(i)
        if fn < 2:
            continue
        for k in range(1, fn):
            transiciones.append({"current_state": f"q_out_{i}_{k}", "read_symbol": "B",
                                 "next_state": f"q_out_{i}_{k+1}", "write_symbol": "1", "move": "R"})
        transiciones.append({"current_state": f"q_out_{i}_{fn}", "read_symbol": "B",
                             "next_state": "q_aceptar", "write_symbol": "1", "move": "N"})

    transiciones.append({"current_state": "q_overflow", "read_symbol": "1",
                         "next_state": "q_overflow", "write_symbol": "B", "move": "R"})
    transiciones.append({"current_state": "q_overflow", "read_symbol": "B",
                         "next_state": "q_aceptar", "write_symbol": "X", "move": "N"})

    vistos = set()
    estadosUnicos: List[str] = []
    for s in estados:
        if s not in vistos:
            vistos.add(s)
            estadosUnicos.append(s)

    return {
        "description": "MT determinista (una cinta) para Fibonacci en unario",
        "purpose": f"Entrada: 1^n. Salida: 1^F(n) para n=0..{maxN}; n>{maxN} escribe X.",
        "example": "111 -> 11  (F(3)=2)",
        "states": estadosUnicos,
        "input_alphabet": ["1"],
        "tape_alphabet": ["1", "0", "X", "B"],
        "initial_state": "q0",
        "accept_states": ["q_aceptar"],
        "blank_symbol": "B",
        "transitions": transiciones,
    }


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
