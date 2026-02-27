# Pruebas manuales

## Prueba 1: F(0) = 0

- **Entrada en cinta:** (vacia -- solo blancos)
- **Resultado esperado:** cinta vacia (sin unos)
- **Estado final esperado:** q_aceptar
- **Pasos esperados:** 0
- **Razon:** caso base, la MT lee B inmediatamente y acepta sin escribir.

## Prueba 2: F(1) = 1

- **Entrada en cinta:** `1`
- **Resultado esperado:** `1`
- **Estado final esperado:** q_aceptar
- **Pasos esperados:** 2
- **Razon:** caso base, la MT lee el unico 1, lo borra, avanza y escribe un 1.

## Prueba 3: F(5) = 5

- **Entrada en cinta:** `11111`
- **Resultado esperado:** `11111` (cinco unos)
- **Estado final esperado:** q_aceptar
- **Pasos esperados:** 10
- **Razon:** caso intermedio. La MT lee 5 unos (5 pasos de lectura) y luego
  recorre 5 estados de escritura produciendo 5 unos.

## Prueba 4: F(7) = 13

- **Entrada en cinta:** `1111111`
- **Resultado esperado:** `1111111111111` (trece unos)
- **Estado final esperado:** q_aceptar
- **Pasos esperados:** 20
- **Razon:** caso mas grande para verificar que la cadena de escritura funciona
  correctamente para valores de Fibonacci mayores que n.

## Prueba 5: Overflow (n = 13)

- **Entrada en cinta:** `1111111111111` (trece unos)
- **Resultado esperado:** `X`
- **Estado final esperado:** q_aceptar
- **Razon:** la MT no soporta n > 12. Debe borrar toda la entrada y escribir X.

## Prueba 6: Entrada negativa (n = -3)

- **Entrada en cinta:** `-111`
- **Resultado esperado:** la MT se detiene sin aceptar
- **Estado final esperado:** q0 (no hay transicion para '-')
- **Razon:** la convencion para negativos establece que la MT rechaza la entrada.

## Como ejecutar las pruebas

```bash
python main.py
```

Seleccionar opcion 1 (con traza) o 2 (sin traza) e metees el valor de n.
Para la prueba de entrada negativa, tomas la opcion 3 (simular otra MT) con el
mismo archivo `configuracion/fibonacci.json` y pones `-111` como cadena.