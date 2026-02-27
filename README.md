# Proyecto 1 — Máquina de Turing: Sucesión de Fibonacci

Simulador de Máquinas de Turing deterministas de una cinta, aplicado al cálculo de la sucesión de Fibonacci con codificación unaria.

## Requisitos

- Python 3.8+
- Dependencias: `matplotlib`, `numpy`, `python-docx`, `pytest`

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

El menú interactivo permite:
1. Calcular F(n) con o sin traza paso a paso
2. Simular cualquier otra MT cargando su archivo JSON
3. Ejecutar benchmark completo (n = 0..12)
4. Generar gráfico de dispersión
5. Generar reporte DOCX

## Generar la configuración de la MT

Si `configuracion/fibonacci.json` no existe:

```bash
python herramientas/generarFibonacciMT.py
```

## Generar diagrama de estados

```bash
python herramientas/generarDiagrama.py
```

Produce `documentos/diagramaFibonacci.png`.
