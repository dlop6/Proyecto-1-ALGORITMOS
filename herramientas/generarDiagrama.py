# Genera el diagrama de estados de la MT de Fibonacci como PNG

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle


def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def dibujarCirculo(ax, x, y, texto, radio=0.35, color="#e8f0fe",
                   bordeColor="#1a73e8", doble=False, fontSize: int = 8):
    c = Circle((x, y), radio, facecolor=color, edgecolor=bordeColor,
                   linewidth=1.5, zorder=3)
    ax.add_patch(c)
    if doble:
        c2 = Circle((x, y), radio * 0.85, facecolor="none",
                         edgecolor=bordeColor, linewidth=1.2, zorder=4)
        ax.add_patch(c2)
    ax.text(x, y, texto, ha="center", va="center", fontsize=fontSize,
            fontweight="bold", zorder=5)


def flecha(ax, x1, y1, x2, y2, etiqueta="", curva=0.0, fontSize=6.5):
    estilo = f"arc3,rad={curva}" if curva else "arc3,rad=0"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#555",
                                connectionstyle=estilo, lw=1.0),
                zorder=2)
    if etiqueta:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        offset = 0.18 if curva == 0 else 0.25
        ax.text(mx, my + offset, etiqueta, ha="center", va="center",
                fontsize=fontSize, color="#333", zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))


def main():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(-1, 17)
    ax.set_ylim(-8.5, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(8, 2.0, "Maquina de Turing - Fibonacci F(n)", ha="center",
            fontsize=14, fontweight="bold", color="#1a73e8")
    ax.text(8, 1.5, "Entrada: 1^n (unario)  ->  Salida: 1^F(n)",
            ha="center", fontsize=9, color="#666")

    r = 0.35
    yLectura = 0.0
    posX = {}
    for i in range(13):
        x = i * 1.2 + 0.5
        posX[f"q{i}"] = (x, yLectura)
        dibujarCirculo(ax, x, yLectura, f"q{i}", radio=r)

    for i in range(12):
        x1 = posX[f"q{i}"][0] + r
        x2 = posX[f"q{i+1}"][0] - r
        flecha(ax, x1, yLectura, x2, yLectura, "1/B,R")

    xOvf = posX["q12"][0] + 1.5
    yOvf = yLectura
    posX["q_overflow"] = (xOvf, yOvf)
    dibujarCirculo(ax, xOvf, yOvf, "q_ovf", radio=r, color="#ffcdd2", bordeColor="#d32f2f")
    flecha(ax, posX["q12"][0] + r, yLectura, xOvf - r, yOvf, "1/B,R")

    xAcep = 7.0
    yAcep = -7.5
    posX["q_aceptar"] = (xAcep, yAcep)
    dibujarCirculo(ax, xAcep, yAcep, "q_aceptar", radio=0.45,
                   color="#c8e6c9", bordeColor="#388e3c", doble=True, fontSize=7)

    flecha(ax, posX["q0"][0], yLectura - r, xAcep - 2.5, yAcep + 0.45,
           "B/B,N  (F(0)=0)", curva=0.1)
    flecha(ax, posX["q1"][0], yLectura - r, xAcep - 2.0, yAcep + 0.45,
           "B/1,N  (F(1)=1)", curva=0.1)
    flecha(ax, posX["q2"][0], yLectura - r, xAcep - 1.5, yAcep + 0.45,
           "B/1,N  (F(2)=1)", curva=0.1)

    flecha(ax, xOvf, yOvf - r, xAcep + 3.0, yAcep + 0.45,
           "B/X,N", curva=-0.2)
    ax.annotate("", xy=(xOvf + 0.1, yOvf + r + 0.05),
                xytext=(xOvf + 0.4, yOvf + r + 0.05),
                arrowprops=dict(arrowstyle="-|>", color="#555",
                                connectionstyle="arc3,rad=-1.5", lw=1.0))
    ax.text(xOvf + 0.6, yOvf + 0.7, "1/B,R", fontsize=6, color="#333")

    casosDetallados = [
        (3, 2), (4, 3), (5, 5), (6, 8), (7, 13),
    ]

    for idx, (n, fn) in enumerate(casosDetallados):
        yFila = -1.5 - idx * 1.2
        xInicio = posX[f"q{n}"][0]

        flecha(ax, xInicio, yLectura - r, xInicio, yFila + r, "B/B,N")

        numNodos = min(fn, 5)
        for k in range(numNodos):
            xk = xInicio + k * 1.0
            nombre = f"out_{n}_{k+1}"
            dibujarCirculo(ax, xk, yFila, nombre, radio=0.28,
                           color="#fff9c4", bordeColor="#f9a825", fontSize=int(5.5))
            if k > 0:
                flecha(ax, xk - 1.0 + 0.28, yFila, xk - 0.28, yFila, "B/1,R", fontSize=5.5)

        if fn > 5:
            xDots = xInicio + numNodos * 1.0 - 0.3
            ax.text(xDots, yFila, "...", fontsize=12, ha="center", va="center", color="#999")
            xUlt = xDots + 0.8
            nombreUlt = f"out_{n}_{fn}"
            dibujarCirculo(ax, xUlt, yFila, nombreUlt, radio=0.28,
                           color="#fff9c4", bordeColor="#f9a825", fontSize=int(5.5))
            xFlechaAcep = xUlt
        else:
            xFlechaAcep = xInicio + (numNodos - 1) * 1.0

        ax.text(xInicio - 0.7, yFila, f"n={n}\nF={fn}", fontsize=7,
                ha="center", va="center", color="#1a73e8", fontweight="bold")

    ax.text(posX["q3"][0] - 0.7, -1.5 - 5 * 1.2 + 0.3,
            "n = 8..12: mismo patrón\n(cadenas de F(n) estados de escritura)",
            fontsize=8, ha="left", va="center", color="#666",
            style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="#f5f5f5", ec="#ccc"))

    ax.annotate("", xy=(posX["q0"][0] - 0.6, yLectura),
                xytext=(posX["q0"][0] - 1.0, yLectura),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5))
    ax.plot(posX["q0"][0] - 1.0, yLectura, "ko", markersize=6)

    leyenda = [
        mpatches.Patch(facecolor="#e8f0fe", edgecolor="#1a73e8", label="Estado de lectura"),
        mpatches.Patch(facecolor="#fff9c4", edgecolor="#f9a825", label="Estado de escritura"),
        mpatches.Patch(facecolor="#c8e6c9", edgecolor="#388e3c", label="Estado de aceptación"),
        mpatches.Patch(facecolor="#ffcdd2", edgecolor="#d32f2f", label="Overflow"),
    ]
    ax.legend(handles=leyenda, loc="upper right", fontsize=8, framealpha=0.9)

    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    rutaPng = os.path.join(raiz, "documentos", "diagramaFibonacci.png")
    os.makedirs(os.path.dirname(rutaPng), exist_ok=True)
    fig.savefig(rutaPng, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Diagrama generado: {rutaPng}")


if __name__ == "__main__":
    main()
