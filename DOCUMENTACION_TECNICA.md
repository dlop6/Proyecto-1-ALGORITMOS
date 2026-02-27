# Documentación Técnica del Proyecto

## 1) Resumen del proyecto

Este repositorio implementa un simulador de Máquina de Turing determinista de una cinta, configurada para calcular la sucesión de Fibonacci en codificación unaria.

- Entrada esperada para Fibonacci: `1^n` (n unos).
- Salida esperada para `0 <= n <= 12`: `1^F(n)`.
- Convención de overflow para `n > 12`: salida `X`.
- Soporta simulación de otras MT cargando otro archivo JSON desde el menú.

---

## 2) Estructura y propósito de archivos

### Núcleo de ejecución

- `main.py`
  - Punto de entrada del programa.
  - Muestra menú interactivo.
  - Ejecuta simulaciones con o sin traza.
  - Ejecuta benchmark y genera CSV.
  - Genera gráfica de dispersión.
  - Invoca el generador del reporte DOCX.

- `simuladorTuring.py`
  - Define la clase `MaquinaDeTuring`.
  - Carga la definición de la MT desde JSON.
  - Ejecuta transiciones paso a paso.
  - Maneja expansión dinámica de cinta.
  - Devuelve contenido útil de cinta (sin blancos de extremos).

### Configuración de la MT

- `configuracion/fibonacci.json`
  - Definición completa de la MT de Fibonacci.
  - Estado actual del archivo:
  - `states`: 389
  - `transitions`: 402
  - `initial_state`: `q0`
  - `accept_states`: `["q_aceptar"]`
  - `blank_symbol`: `B`
  - `input_alphabet`: `["1"]`
  - `tape_alphabet`: `["1", "0", "X", "B"]`

### Scripts de generación

- `herramientas/generarFibonacciMT.py`
  - Genera `configuracion/fibonacci.json` para `maxN=12`.
  - Construye estados de lectura `q0..q12`, estados de salida `q_out_*`, aceptación y overflow.

- `herramientas/generarDiagrama.py`
  - Genera `documentos/diagramaFibonacci.png`.
  - Dibuja estructura de estados y patrón de transiciones.

- `herramientas/generarReporte.py`
  - Genera `documentos/reporteProyecto.docx`.
  - Usa configuración JSON, CSV de benchmark y gráficas para construir el reporte.

### Pruebas y documentación auxiliar

- `tests/test_fibonacci_mt.py`
  - Suite principal de pruebas automatizadas.
  - Contiene 38 pruebas (`def test_*`).

- `tests/README_TESTS.md`
  - Resumen de cobertura y ejecución de pruebas.

- `documentos/pruebasManuales.md`
  - Casos manuales definidos para validación funcional.

### Resultados y artefactos

- `analisis/resultadosBenchmark.csv`
  - Salida del benchmark oficial del menú (n=0..12, 3 repeticiones).

- `analisis/resultadosBenchmark_tmp.csv`
  - Archivo adicional de benchmark temporal (presente actualmente en el repo).

- `analisis/dispersionTiempo.png`
  - Gráfica de dispersión y ajuste cuadrático sobre tiempos medidos.

- `documentos/diagramaFibonacci.png`
  - Diagrama de estados de la MT de Fibonacci.

- `documentos/reporteProyecto.docx`
  - Reporte del proyecto en formato Word.

### Configuración del proyecto

- `requirements.txt`
  - Paquetes declarados: `matplotlib`, `numpy`, `python-docx`, `pytest`.

- `README.md`
  - Guía breve de instalación y ejecución.

---

## 3) Flujo de ejecución del programa

1. Se ejecuta `main.py`.
2. El menú ofrece:
   - Calcular Fibonacci con traza.
   - Calcular Fibonacci sin traza.
   - Simular otra MT cargando otro JSON.
   - Ejecutar benchmark.
   - Generar gráfica de dispersión.
   - Generar reporte DOCX.
3. Para simular, `main.py` llama a `ejecutarSimulacion(...)`.
4. `ejecutarSimulacion(...)` instancia `MaquinaDeTuring` desde `simuladorTuring.py`.
5. La máquina:
   - Carga JSON.
   - Inicializa cinta y estado.
   - Ejecuta pasos hasta aceptar, detenerse sin transición, o alcanzar límite.
6. Se imprime resultado final:
   - salida de cinta,
   - estado final,
   - pasos,
   - tiempo.

---

## 4) Convenciones de entrada y salida

### Entrada válida para Fibonacci

- `n=0` se representa como cadena vacía `""`.
- `n>0` se representa como `1` repetido `n` veces.

Ejemplos:

- `n=3` -> `111`
- `n=5` -> `11111`

### Entradas no válidas o fuera de convención

- Negativo (ejemplo `-111`): no existe transición desde `q0` para `-`, se detiene sin aceptar.
- Símbolos fuera de alfabeto de entrada (ejemplo `abc`, `1a1`): se detiene sin aceptar al no encontrar transición aplicable.

### Criterio de aceptación y detención

- Acepta si el estado final está en `accept_states` (`q_aceptar`).
- Se detiene sin aceptar si no hay transición para `(estado, símbolo)`.
- También puede detenerse por límite de pasos (`maxPasos`).

---

## 5) Formato de traza de simulación

Cuando la traza está activa, cada paso muestra:

- número de paso,
- estado actual,
- posición de cabeza,
- contenido de cinta.

Formato impreso:

`Paso <n> | Estado: <estado> | Cabeza: <pos> | Cinta: <símbolos>`

---

## 6) Resultados medidos (benchmark actual)

Fuente: `analisis/resultadosBenchmark.csv` (13 filas, `n=0..12`).

| n | \|entrada\| | pasosPromedio | tiempoPromSeg | \|salida\| | aceptada |
|---:|---:|---:|---:|---:|:---:|
| 0 | 0 | 1.0 | 0.000013449 | 0 | True |
| 1 | 1 | 2.0 | 0.000015769 | 1 | True |
| 2 | 2 | 3.0 | 0.000014440 | 1 | True |
| 3 | 3 | 6.0 | 0.000022472 | 2 | True |
| 4 | 4 | 8.0 | 0.000023995 | 3 | True |
| 5 | 5 | 11.0 | 0.000026471 | 5 | True |
| 6 | 6 | 15.0 | 0.000042762 | 8 | True |
| 7 | 7 | 21.0 | 0.000057265 | 13 | True |
| 8 | 8 | 30.0 | 0.000090414 | 21 | True |
| 9 | 9 | 44.0 | 0.000211055 | 34 | True |
| 10 | 10 | 66.0 | 0.000344951 | 55 | True |
| 11 | 11 | 101.0 | 0.000796467 | 89 | True |
| 12 | 12 | 157.0 | 0.002313792 | 144 | True |

Resumen objetivo de ese CSV:

- Todas las ejecuciones registradas están aceptadas (`True`).
- `|salida|` coincide con `F(n)` para `n=0..12`.
- El máximo de pasos registrado es `157` (en `n=12`).
- El tiempo máximo registrado es `0.0023137923368873694 s` (en `n=12`).

---

## 7) Regresión reportada en benchmark

Con los datos de `analisis/resultadosBenchmark.csv`, el ajuste cuadrático usado por el proyecto da:

`T(n) ~= 0.0000283985*n^2 + -0.0002322267*n + 0.0002790759`

La gráfica correspondiente se guarda en:

- `analisis/dispersionTiempo.png`

---

## 8) Comportamiento para overflow y entradas no válidas

### Overflow (`n > 12`)

Casos verificados en ejecución:

- `n=13`, `14`, `20`, `50`, `100`, `500`, `1000` terminan en `q_aceptar` y salida `X`.

### Entradas inválidas

Ejemplos observados:

- `-111` -> estado final `q0`, `pasos=0`, detenida sin transición aplicable.
- `abc` -> estado final `q0`, `pasos=0`, detenida sin transición aplicable.
- `1a1` -> avanza parcialmente y luego se detiene sin transición aplicable.

---

## 9) Suite de pruebas

Archivo: `tests/test_fibonacci_mt.py`

Cobertura por categorías:

- Casos básicos de Fibonacci.
- Casos intermedios `n=4..12`.
- Casos edge: overflow e inválidos.
- Consistencia completa `n=0..12`.
- Validación de integridad del CSV.
- Integración de API de simulación.
- Validación estructural del JSON.

Cantidad de pruebas declaradas:

- 38 funciones `test_*`.

Nota de entorno actual:

- En este entorno no fue posible ejecutar `pytest` porque el módulo no está instalado (`No module named pytest`).
- El proyecto sí declara `pytest` en `requirements.txt`.

---

## 10) Cómo reproducir todo desde cero

### Dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar programa principal

```bash
python3 main.py
```

### Regenerar JSON de la MT

```bash
python3 herramientas/generarFibonacciMT.py
```

### Regenerar diagrama

```bash
python3 herramientas/generarDiagrama.py
```

### Ejecutar benchmark (desde menú, opción 4)

Salida esperada:

- `analisis/resultadosBenchmark.csv`

### Generar gráfica (desde menú, opción 5)

Salida esperada:

- `analisis/dispersionTiempo.png`

### Generar reporte DOCX (desde menú, opción 6)

Salida esperada:

- `documentos/reporteProyecto.docx`

### Ejecutar pruebas

```bash
python3 -m pytest tests/test_fibonacci_mt.py -v
```

---

## 11) Estado actual de artefactos en el repositorio

Archivos de salida presentes y su tamaño aproximado:

- `analisis/resultadosBenchmark.csv` (~995 bytes)
- `analisis/resultadosBenchmark_tmp.csv` (~993 bytes)
- `analisis/dispersionTiempo.png` (~65 KB)
- `documentos/diagramaFibonacci.png` (~167 KB)
- `documentos/reporteProyecto.docx` (~445 KB)

---

## 12) Observaciones técnicas importantes

- El comando usado en `README.md` es `python main.py`, pero en este entorno la ejecución funcional fue con `python3 main.py`.
- La opción 3 del menú (`Simular otra MT`) es la parte que cumple la generalidad pedida por el enunciado: cargar cualquier MT determinista de una cinta desde JSON.
- El simulador no se queda en ejecución infinita por diseño de control de pasos (`maxPasos`) y por transiciones definidas para overflow.
