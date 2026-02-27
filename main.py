# Punto de entrada del simulador de Máquinas de Turing.

import sys, os, time, csv
from typing import List, Dict, Tuple, Any

from simuladorTuring import MaquinaDeTuring


#utils

def limpiarPantalla():
    os.system("cls" if os.name == "nt" else "clear")


def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def formatearCinta(mt: MaquinaDeTuring) -> str:
    return " ".join(mt.cinta)


def imprimirPaso(mt: MaquinaDeTuring, nPaso: int) -> None:
    print(f"  Paso {nPaso:>4}  |  Estado: {mt.estadoActual:<16}"
          f"  |  Cabeza: {mt.posicionCabeza:<4}"
          f"  |  Cinta: {formatearCinta(mt)}")


def ejecutarSimulacion(rutaConfig: str, entrada: str,
                       maxPasos: int, traza: bool) -> Dict[str, Any]:
    """Carga la MT, la ejecuta y devuelve diccionario de resultados."""
    mt = MaquinaDeTuring(rutaConfig)
    t0 = time.perf_counter()
    mt.inicializarCinta(entrada)

    if traza:
        print("-" * 80)
        imprimirPaso(mt, 0)

    limiteAlcanzado = detenidaSinAceptar = False

    while mt.pasosEjecutados < maxPasos:
        if mt.estadoActual in mt.estadosAceptacion:
            break
        avanzo = mt.ejecutarPaso()
        if traza and avanzo:
            imprimirPaso(mt, mt.pasosEjecutados)
        if not avanzo:
            detenidaSinAceptar = True
            break

    if mt.pasosEjecutados >= maxPasos and mt.estadoActual not in mt.estadosAceptacion:
        limiteAlcanzado = True

    t1 = time.perf_counter()
    if traza:
        print("-" * 80)

    return {
        "salida": mt.obtenerContenidoCinta(),
        "estadoFinal": mt.estadoActual,
        "pasos": mt.pasosEjecutados,
        "tiempoSeg": t1 - t0,
        "aceptada": mt.estadoActual in mt.estadosAceptacion,
        "limiteAlcanzado": limiteAlcanzado,
        "detenidaSinAceptar": detenidaSinAceptar,
    }


def mostrarResultado(res: Dict[str, Any]) -> None:
    print()
    print(f"  Resultado de la cinta : {res['salida']}")
    print(f"  Estado final          : {res['estadoFinal']}")
    print(f"  Pasos ejecutados      : {res['pasos']}")
    print(f"  Tiempo                : {float(res['tiempoSeg']):.6f} s")
    print()
    if res["aceptada"]:
        print("  >> Estado de aceptación alcanzado.")
    elif res["limiteAlcanzado"]:
        print("  >> Detenida por límite de pasos.")
    elif res["detenidaSinAceptar"]:
        print("  >> Detenida: no hay transición aplicable.")


#regresión cuadrática

def promedio(v: List[float]) -> float:
    return sum(v) / len(v) if v else 0.0


def resolver3x3(a: list, b: list) -> tuple:
    def det3(m: list) -> float:
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
                - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
                + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))  # type: ignore[return-value]
    d = det3(a)
    if d == 0:
        return 0.0, 0.0, 0.0
    ax = [[float(b[0]),float(a[0][1]),float(a[0][2])],[float(b[1]),float(a[1][1]),float(a[1][2])],[float(b[2]),float(a[2][1]),float(a[2][2])]]
    ay = [[float(a[0][0]),float(b[0]),float(a[0][2])],[float(a[1][0]),float(b[1]),float(a[1][2])],[float(a[2][0]),float(b[2]),float(a[2][2])]]
    az = [[float(a[0][0]),float(a[0][1]),float(b[0])],[float(a[1][0]),float(a[1][1]),float(b[1])],[float(a[2][0]),float(a[2][1]),float(b[2])]]
    return det3(ax)/d, det3(ay)/d, det3(az)/d  # type: ignore[return-value]


def regresionCuadratica(puntos: List[Tuple[float, float]]) -> Tuple[float, float, float]:
    if not puntos:
        return 0.0, 0.0, 0.0
    sx  = sum(x for x,_ in puntos)
    sx2 = sum(x**2 for x,_ in puntos)
    sx3 = sum(x**3 for x,_ in puntos)
    sx4 = sum(x**4 for x,_ in puntos)
    sy  = sum(y for _,y in puntos)
    sxy = sum(x*y for x,y in puntos)
    sx2y= sum(x**2*y for x,y in puntos)
    n   = float(len(puntos))
    return resolver3x3([[sx4,sx3,sx2],[sx3,sx2,sx],[sx2,sx,n]],[sx2y,sxy,sy])


#benchmark

def ejecutarBenchmark(rutaConfig: str, maxN: int = 12,
                      repeticiones: int = 3, maxPasos: int = 200000,
                      rutaCsv: str = "analisis/resultadosBenchmark.csv") -> List[Dict[str, Any]]:
    """Ejecuta la MT para n=0..maxN y guarda CSV."""
    filas: List[Dict[str, Any]] = []
    print("=" * 70)
    print(f"  BENCHMARK   n = 0 .. {maxN}   ({repeticiones} repeticiones)")
    print("=" * 70)

    for n in range(maxN + 1):
        entrada = "1" * n
        tiempos: List[float] = []
        pasos: List[float] = []
        ultimaSalida = ""
        aceptada = True

        for _ in range(repeticiones):
            r = ejecutarSimulacion(rutaConfig, entrada, maxPasos, traza=False)
            tiempos.append(float(r["tiempoSeg"]))
            pasos.append(float(r["pasos"]))
            ultimaSalida = str(r["salida"])
            aceptada = aceptada and bool(r["aceptada"])

        fila = {
            "n": n,
            "entrada": entrada,
            "tiempoPromSeg": promedio(tiempos),
            "pasosPromedio": promedio(pasos),
            "salida": ultimaSalida,
            "aceptada": aceptada,
        }
        filas.append(fila)
        print(f"  n={n:>2}  |  pasos={fila['pasosPromedio']:>8.1f}"
              f"  |  t={fila['tiempoPromSeg']:.6f} s"
              f"  |  |salida|={len(ultimaSalida):>3}"
              f"  |  F(n)={fibonacci(n):>3}  "
              f"{'OK' if len(ultimaSalida) == fibonacci(n) else 'FAIL'}")

    dirSalida = os.path.dirname(rutaCsv)
    if dirSalida:
        os.makedirs(dirSalida, exist_ok=True)
    with open(rutaCsv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["n","entrada","tiempoPromSeg",
                                          "pasosPromedio","salida","aceptada"])
        w.writeheader()
        w.writerows(filas)

    puntos = [(float(r["n"]), float(r["tiempoPromSeg"])) for r in filas]
    a, b, c = regresionCuadratica(puntos)
    print("-" * 70)
    print(f"  CSV: {rutaCsv}")
    print(f"  T(n) ~= {a:.10f}*n^2 + {b:.10f}*n + {c:.10f}")
    print("=" * 70)
    return filas


#gen de gráfico

def generarGraficoDispersion(rutaCsv: str, rutaPng: str) -> bool:
    """Lee el CSV y genera el scatter plot con matplotlib."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("  matplotlib/numpy no disponible. Instale: pip install matplotlib")
        return False

    filas = []
    with open(rutaCsv, "r", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            filas.append({"n": int(fila["n"]),
                          "t": float(fila["tiempoPromSeg"])})

    ns = [r["n"] for r in filas]
    ts = [r["t"] for r in filas]
    puntos = [(float(r["n"]), r["t"]) for r in filas]
    a, b, c = regresionCuadratica(puntos)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(ns, ts, color="#2563eb", zorder=5, label="Datos medidos")
    xf = np.linspace(0, max(ns), 200)
    # Un polinomio de ajuste puede predecir valores negativos en tramos cortos;
    # se recorta a 0 porque el tiempo físico no puede ser negativo.
    yfit = np.maximum(a*xf**2 + b*xf + c, 0.0)
    ax.plot(xf, yfit, color="#dc2626", linewidth=1.5,
            label=f"Regresion: {a:.2e}n^2 + {b:.2e}n + {c:.2e}")
    ax.set_xlabel("n (tamaño de entrada)")
    ax.set_ylabel("Tiempo promedio (s)")
    ax.set_title("Tiempo de ejecución vs tamaño de entrada")
    ax.set_ylim(bottom=0.0)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(rutaPng, dpi=150)
    plt.close(fig)
    print(f"  Gráfico guardado: {rutaPng}")
    return True


#menu

RUTA_CONFIG = os.path.join("configuracion", "fibonacci.json")
RUTA_CSV    = os.path.join("analisis", "resultadosBenchmark.csv")
RUTA_PNG    = os.path.join("analisis", "dispersionTiempo.png")


def mostrarMenu():
    print()
    print("+---------------------------------------------+")
    print("|   Simulador de Maquina de Turing            |")
    print("|   Sucesion de Fibonacci                     |")
    print("+---------------------------------------------+")
    print("|                                             |")
    print("|   1.  Calcular F(n) -- con traza            |")
    print("|   2.  Calcular F(n) -- sin traza            |")
    print("|   3.  Simular otra MT (cargar JSON)         |")
    print("|   4.  Ejecutar benchmark (n = 0..12)        |")
    print("|   5.  Generar grafico de dispersion         |")
    print("|   6.  Generar reporte DOCX                  |")
    print("|                                             |")
    print("|   0.  Salir                                 |")
    print("|                                             |")
    print("+---------------------------------------------+")


def pedirN() -> int:
    while True:
        try:
            n = int(input("\n  Ingrese n (0-12): "))
            if 0 <= n <= 12:
                return n
            print("  Valor fuera de rango (0-12).")
        except ValueError:
            print("  Ingrese un número entero.")


def opcionFibonacci(conTraza: bool):
    if not os.path.isfile(RUTA_CONFIG):
        print(f"\n  No se encontró {RUTA_CONFIG}.")
        print("  Ejecute: python herramientas/generarFibonacciMT.py")
        return

    n = pedirN()
    entrada = "1" * n
    print(f"\n  Ejecutando MT con n = {n}  (entrada: '{entrada}')")
    print(f"  F({n}) esperado = {fibonacci(n)}\n")

    res = ejecutarSimulacion(RUTA_CONFIG, entrada, maxPasos=200000, traza=conTraza)
    mostrarResultado(res)

    longSalida = len(str(res["salida"]))
    esperado = fibonacci(n)
    if longSalida == esperado:
        print(f"  Verificacion: |salida| = {longSalida} = F({n})  OK")
    else:
        print(f"  Verificacion: |salida| = {longSalida} != F({n}) = {esperado}  FAIL")


def opcionOtraMT():
    ruta = input("\n  Ruta al archivo JSON de la MT: ").strip()
    if not os.path.isfile(ruta):
        print(f"  No se encontró: {ruta}")
        return
    entrada = input("  Cadena de entrada: ").strip()
    maxP = input("  Máx. pasos [10000]: ").strip()
    maxP = int(maxP) if maxP.isdigit() else 10000
    traza = input("  ¿Mostrar traza? (s/n) [s]: ").strip().lower()
    conTraza = traza != "n"

    res = ejecutarSimulacion(ruta, entrada, maxP, conTraza)
    mostrarResultado(res)


def opcionBenchmark():
    if not os.path.isfile(RUTA_CONFIG):
        print(f"\n  No se encontró {RUTA_CONFIG}.")
        return
    ejecutarBenchmark(RUTA_CONFIG, maxN=12, repeticiones=3,
                      maxPasos=200000, rutaCsv=RUTA_CSV)


def opcionGrafico():
    if not os.path.isfile(RUTA_CSV):
        print(f"\n  No se encontró {RUTA_CSV}. Ejecute el benchmark primero.")
        return
    generarGraficoDispersion(RUTA_CSV, RUTA_PNG)


def opcionReporte():
    rutaScript = os.path.join("herramientas", "generarReporte.py")
    if not os.path.isfile(rutaScript):
        print(f"\n  No se encontró {rutaScript}.")
        return
    os.system(f'python "{rutaScript}"')


def menuPrincipal():
    while True:
        mostrarMenu()
        opcion = input("\n  Seleccione una opción: ").strip()

        if opcion == "1":
            opcionFibonacci(conTraza=True)
        elif opcion == "2":
            opcionFibonacci(conTraza=False)
        elif opcion == "3":
            opcionOtraMT()
        elif opcion == "4":
            opcionBenchmark()
        elif opcion == "5":
            opcionGrafico()
        elif opcion == "6":
            opcionReporte()
        elif opcion == "0":
            print("\n  Hasta luego!\n")
            break
        else:
            print("\n  Opción no válida.")

        input("\n  Presione Enter para continuar...")
        limpiarPantalla()


if __name__ == "__main__":
    menuPrincipal()
