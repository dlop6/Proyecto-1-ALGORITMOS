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


