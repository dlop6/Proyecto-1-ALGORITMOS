# 🧪 Suite de Testing - Máquina de Turing Fibonacci

## ✅ Resumen de Ejecución

**Total de tests: 38**  
**Tests pasados: 38 (100%)**  
**Tests fallidos: 0**  
**Tiempo de ejecución: 0.18s**

---

## 📦 Cobertura de Testing

### 1️⃣ **Casos Básicos** (6 tests)
Tests basados en `documentos/pruebasManuales.md`:
- ✅ F(0) = 0 - Entrada vacía
- ✅ F(1) = 1 - Caso base
- ✅ F(2) = 1 - Caso base  
- ✅ F(3) = 2 - Caso intermedio pequeño
- ✅ F(5) = 5 - Caso de prueba manual
- ✅ F(7) = 13 - Caso de prueba manual grande

### 2️⃣ **Casos Normales Intermedios** (7 tests)
Validación completa de n=4 a n=12:
- ✅ F(4) = 3
- ✅ F(6) = 8
- ✅ F(8) = 21
- ✅ F(9) = 34
- ✅ F(10) = 55
- ✅ F(11) = 89
- ✅ F(12) = 144 (valor máximo soportado)

### 3️⃣ **Casos Edge** (6 tests)
Pruebas de límites y entradas inválidas:
- ✅ Overflow n=13 → X
- ✅ Overflow n=14 → X
- ✅ Overflow n=20 → X
- ✅ Entrada negativa "-111" → rechazada
- ✅ Símbolos inválidos "abc" → rechazada
- ✅ Entrada mixta "1a1" → rechazada

### 4️⃣ **Consistencia Completa** (3 tests)
Validación exhaustiva:
- ✅ Todos los valores F(0)..F(12) correctos
- ✅ Todos terminan en estado `q_aceptar`
- ✅ Ninguno excede límite de pasos (200,000)

### 5️⃣ **Validación del CSV de Benchmark** (7 tests)
Integridad de `analisis/resultadosBenchmark.csv`:
- ✅ Archivo existe
- ✅ Contiene 13 filas (n=0..12)
- ✅ Valores de n correctos (0, 1, 2, ..., 12)
- ✅ Salidas tienen longitud = F(n)
- ✅ Todas marcadas como "aceptada=True"
- ✅ Tiempos crecen con n
- ✅ Pasos crecen con n

### 6️⃣ **Integración del Simulador** (4 tests)
Tests de la función `ejecutarSimulacion()`:
- ✅ Ejecución con traza no crashea
- ✅ Ejecución sin traza no crashea
- ✅ Devuelve estructura correcta (7 claves)
- ✅ Límite de pasos funciona

### 7️⃣ **Validación de Configuración JSON** (5 tests)
Verificación de `configuracion/fibonacci.json`:
- ✅ Archivo existe
- ✅ Tiene estado inicial "q0"
- ✅ Tiene estados de aceptación ["q_aceptar"]
- ✅ Tiene transiciones definidas
- ✅ Tiene símbolo blanco "B"

---

## 🚀 Cómo Ejecutar los Tests

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar todos los tests
```bash
python -m pytest tests/test_fibonacci_mt.py -v
```

### Ejecutar tests con más detalle
```bash
python -m pytest tests/test_fibonacci_mt.py -v --tb=long
```

### Ejecutar una clase específica de tests
```bash
python -m pytest tests/test_fibonacci_mt.py::TestCasosBasicos -v
```

### Ejecutar un test individual
```bash
python -m pytest tests/test_fibonacci_mt.py::TestCasosBasicos::test_f5_intermedio -v
```

---

## 📊 Resultados por Categoría

| Categoría | Tests | Pasados | Comentario |
|-----------|-------|---------|------------|
| Casos Básicos | 6 | 6 | ✅ Todos los casos manuales funcionan |
| Casos Intermedios | 7 | 7 | ✅ Cobertura completa n=4..12 |
| Casos Edge | 6 | 6 | ✅ Manejo correcto de overflow y errores |
| Consistencia | 3 | 3 | ✅ Todos los valores validados |
| Benchmark CSV | 7 | 7 | ✅ Datos coherentes y correctos |
| Integración | 4 | 4 | ✅ API funcional |
| Configuración | 5 | 5 | ✅ JSON bien formado |

---

## 🔍 Conclusiones

1. **El simulador funciona correctamente** para todos los casos de prueba
2. **Los datos del benchmark son coherentes** con los valores esperados
3. **El manejo de errores es robusto** (entradas inválidas, overflow)
4. **La configuración JSON está completa** y bien estructurada
5. **No se detectaron inconsistencias** entre código, datos y documentación

---

## 📝 Notas Adicionales

- **Tiempo de ejecución**: Los tests completos corren en menos de 0.2 segundos
- **Cobertura**: Se probaron 19 valores diferentes de entrada (n=0..20)
- **Edge cases**: Se validaron 6 escenarios de error diferentes
- **Validación de datos**: Se verificó la consistencia de 13 filas del CSV

---

## ⚙️ Estructura de los Tests

```
tests/
├── __init__.py
├── test_fibonacci_mt.py  # Suite completa (38 tests)
└── README_TESTS.md       # Este archivo
```

Cada clase de tests está organizada por propósito:
- `TestCasosBasicos` - Casos fundamentales
- `TestCasosNormalesIntermedios` - Cobertura completa
- `TestCasosEdge` - Límites y errores
- `TestConsistenciaCompleta` - Validación exhaustiva
- `TestBenchmarkCSV` - Integridad de datos
- `TestSimuladorIntegracion` - API y funciones
- `TestConfiguracionJSON` - Configuración válida
