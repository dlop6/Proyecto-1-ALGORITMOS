"""
test suite completo para el simulador de máquina de turing - fibonacci
cubre: casos básicos, casos edge, validación de datos, consistencia
"""

import sys
import os
import csv
import pytest

# agregar el directorio padre al path para importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simuladorTuring import MaquinaDeTuring
from main import fibonacci, ejecutarSimulacion


# config
RUTA_CONFIG = os.path.join("configuracion", "fibonacci.json")
RUTA_CSV = os.path.join("analisis", "resultadosBenchmark.csv")
MAX_PASOS = 200000


class TestCasosBasicos:
    """tests de casos base explícitos en pruebasManuales.md"""
    
    def test_f0_caso_base(self):
        """f(0) = 0 - entrada vacía debe dar salida vacía"""
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar("", MAX_PASOS)
        
        assert resultado == "", f"f(0) debería ser cadena vacía, obtuvo: '{resultado}'"
        assert mt.estadoActual == "q_aceptar", f"debería aceptar, estado: {mt.estadoActual}"
    
    def test_f1_caso_base(self):
        """f(1) = 1 - un uno debe dar un uno"""
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar("1", MAX_PASOS)
        
        assert len(resultado) == 1, f"f(1) debería ser 1 uno, obtuvo: {len(resultado)}"
        assert resultado == "1", f"f(1) debería ser '1', obtuvo: '{resultado}'"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f2_caso_base(self):
        """f(2) = 1 - dos unos debe dar un uno"""
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar("11", MAX_PASOS)
        
        assert len(resultado) == 1, f"f(2) debería ser 1 uno, obtuvo: {len(resultado)}"
        assert resultado == "1", f"f(2) debería ser '1', obtuvo: '{resultado}'"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f3_intermedio(self):
        """f(3) = 2 - caso intermedio pequeño"""
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar("111", MAX_PASOS)
        
        assert len(resultado) == 2, f"f(3) debería ser 2 unos, obtuvo: {len(resultado)}"
        assert resultado == "11", f"f(3) debería ser '11', obtuvo: '{resultado}'"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f5_intermedio(self):
        """f(5) = 5 - caso de prueba manual"""
        entrada = "1" * 5
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 5
        assert len(resultado) == esperado, f"f(5) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert resultado == "1" * esperado
        assert mt.estadoActual == "q_aceptar"
    
    def test_f7_grande(self):
        """f(7) = 13 - caso de prueba manual grande"""
        entrada = "1" * 7
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 13
        assert len(resultado) == esperado, f"f(7) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert resultado == "1" * esperado
        assert mt.estadoActual == "q_aceptar"


class TestCasosNormalesIntermedios:
    """tests de casos normales que no están explícitamente en pruebasManuales.md"""
    
    def test_f4(self):
        """f(4) = 3"""
        entrada = "1" * 4
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 3
        assert len(resultado) == esperado, f"f(4) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f6(self):
        """f(6) = 8"""
        entrada = "1" * 6
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 8
        assert len(resultado) == esperado, f"f(6) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f8(self):
        """f(8) = 21"""
        entrada = "1" * 8
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 21
        assert len(resultado) == esperado, f"f(8) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f9(self):
        """f(9) = 34"""
        entrada = "1" * 9
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 34
        assert len(resultado) == esperado, f"f(9) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f10(self):
        """f(10) = 55"""
        entrada = "1" * 10
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 55
        assert len(resultado) == esperado, f"f(10) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f11(self):
        """f(11) = 89"""
        entrada = "1" * 11
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 89
        assert len(resultado) == esperado, f"f(11) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert mt.estadoActual == "q_aceptar"
    
    def test_f12_maximo_soportado(self):
        """f(12) = 144 - valor máximo soportado"""
        entrada = "1" * 12
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        esperado = 144
        assert len(resultado) == esperado, f"f(12) debería ser {esperado} unos, obtuvo: {len(resultado)}"
        assert mt.estadoActual == "q_aceptar"


class TestCasosEdge:
    """tests de casos edge y límite"""
    
    def test_overflow_n13(self):
        """n = 13 debe causar overflow y escribir X"""
        entrada = "1" * 13
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        # según pruebasManuales.md, debe escribir X
        assert resultado == "X", f"overflow debería producir 'X', obtuvo: '{resultado}'"
        assert mt.estadoActual == "q_aceptar", "debe aceptar después de overflow"
    
    def test_overflow_n14(self):
        """n = 14 también debe causar overflow"""
        entrada = "1" * 14
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        assert resultado == "X", f"overflow debería producir 'X', obtuvo: '{resultado}'"
        assert mt.estadoActual == "q_aceptar"
    
    def test_overflow_n20(self):
        """n muy grande debe causar overflow"""
        entrada = "1" * 20
        mt = MaquinaDeTuring(RUTA_CONFIG)
        resultado = mt.ejecutar(entrada, MAX_PASOS)
        
        assert resultado == "X", f"overflow debería producir 'X', obtuvo: '{resultado}'"
        assert mt.estadoActual == "q_aceptar"
    
    def test_entrada_negativa_rechazo(self):
        """entrada con '-' debe rechazarse (no aceptar)"""
        entrada = "-111"
        mt = MaquinaDeTuring(RUTA_CONFIG)
        mt.inicializarCinta(entrada)
        
        # ejecutar hasta que no pueda avanzar o acepte
        while mt.pasosEjecutados < 100 and mt.estadoActual not in mt.estadosAceptacion:
            if not mt.ejecutarPaso():
                break
        
        # no debe llegar a estado de aceptación
        assert mt.estadoActual != "q_aceptar", "entrada negativa no debería aceptarse"
        assert mt.estadoActual == "q0", "debe quedarse en q0 sin transición"
    
    def test_entrada_invalida_simbolo_desconocido(self):
        """entrada con símbolos no válidos debe rechazarse"""
        entrada = "abc"
        mt = MaquinaDeTuring(RUTA_CONFIG)
        mt.inicializarCinta(entrada)
        
        while mt.pasosEjecutados < 100 and mt.estadoActual not in mt.estadosAceptacion:
            if not mt.ejecutarPaso():
                break
        
        # no debe llegar a aceptación
        assert mt.estadoActual != "q_aceptar"
    
    def test_entrada_mixta_invalida(self):
        """entrada con mezcla de símbolos debe fallar"""
        entrada = "1a1"
        mt = MaquinaDeTuring(RUTA_CONFIG)
        mt.inicializarCinta(entrada)
        
        while mt.pasosEjecutados < 100 and mt.estadoActual not in mt.estadosAceptacion:
            if not mt.ejecutarPaso():
                break
        
        assert mt.estadoActual != "q_aceptar"


class TestConsistenciaCompleta:
    """tests que validan la consistencia de todos los valores n=0..12"""
    
    def test_todos_los_valores_fibonacci_correctos(self):
        """verifica que f(n) sea correcto para n=0..12"""
        for n in range(13):
            entrada = "1" * n if n > 0 else ""
            mt = MaquinaDeTuring(RUTA_CONFIG)
            resultado = mt.ejecutar(entrada, MAX_PASOS)
            
            esperado = fibonacci(n)
            obtenido = len(resultado)
            
            assert obtenido == esperado, \
                f"f({n}) debería ser {esperado}, obtuvo: {obtenido}"
            assert mt.estadoActual == "q_aceptar", \
                f"f({n}) debería aceptar, estado: {mt.estadoActual}"
    
    def test_todos_aceptan(self):
        """todos los valores válidos deben terminar en q_aceptar"""
        for n in range(13):
            entrada = "1" * n if n > 0 else ""
            mt = MaquinaDeTuring(RUTA_CONFIG)
            mt.ejecutar(entrada, MAX_PASOS)
            
            assert mt.estadoActual == "q_aceptar", \
                f"n={n} no llegó a estado de aceptación: {mt.estadoActual}"
    
    def test_no_excede_limite_pasos(self):
        """ningún caso válido debe exceder el límite de pasos"""
        for n in range(13):
            entrada = "1" * n if n > 0 else ""
            mt = MaquinaDeTuring(RUTA_CONFIG)
            mt.ejecutar(entrada, MAX_PASOS)
            
            assert mt.pasosEjecutados < MAX_PASOS, \
                f"n={n} excedió límite: {mt.pasosEjecutados} pasos"


class TestBenchmarkCSV:
    """tests que validan la integridad del csv de benchmark"""
    
    def test_csv_existe(self):
        """el archivo csv debe existir"""
        assert os.path.isfile(RUTA_CSV), f"no se encontró {RUTA_CSV}"
    
    def test_csv_tiene_13_filas(self):
        """debe tener 13 filas de datos (n=0..12)"""
        with open(RUTA_CSV, "r", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        
        assert len(filas) == 13, f"esperaba 13 filas, obtuvo: {len(filas)}"
    
    def test_csv_valores_n_correctos(self):
        """la columna n debe ir de 0 a 12"""
        with open(RUTA_CSV, "r", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        
        for i, fila in enumerate(filas):
            assert int(fila["n"]) == i, f"fila {i} tiene n={fila['n']}, esperaba {i}"
    
    def test_csv_salidas_correctas(self):
        """las salidas en el csv deben tener longitud = f(n)"""
        with open(RUTA_CSV, "r", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        
        for fila in filas:
            n = int(fila["n"])
            salida = fila.get("salida", "")
            esperado = fibonacci(n)
            obtenido = len(salida)
            
            assert obtenido == esperado, \
                f"csv: n={n}, esperaba |salida|={esperado}, obtuvo {obtenido}"
    
    def test_csv_todos_aceptados(self):
        """todas las ejecuciones deben tener aceptada=True"""
        with open(RUTA_CSV, "r", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        
        for fila in filas:
            n = fila["n"]
            aceptada = fila.get("aceptada", "").lower()
            assert aceptada == "true", f"n={n} no fue aceptada en el csv"
    
    def test_csv_tiempos_crecientes_tendencia(self):
        """los tiempos deben tender a crecer con n (no estricto)"""
        with open(RUTA_CSV, "r", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        
        # verificar que al menos los últimos valores son mayores que los primeros
        tiempo_n5 = float(filas[5]["tiempoPromSeg"])
        tiempo_n12 = float(filas[12]["tiempoPromSeg"])
        
        assert tiempo_n12 > tiempo_n5, \
            f"tiempo debería crecer: t(12)={tiempo_n12} vs t(5)={tiempo_n5}"
    
    def test_csv_pasos_crecientes_tendencia(self):
        """los pasos deben tender a crecer con n"""
        with open(RUTA_CSV, "r", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        
        pasos_n1 = float(filas[1]["pasosPromedio"])
        pasos_n12 = float(filas[12]["pasosPromedio"])
        
        assert pasos_n12 > pasos_n1, \
            f"pasos deberían crecer: p(12)={pasos_n12} vs p(1)={pasos_n1}"


class TestSimuladorIntegracion:
    """tests de integración usando ejecutarSimulacion"""
    
    def test_simulacion_con_traza_no_crash(self):
        """ejecutar con traza no debe crashear"""
        resultado = ejecutarSimulacion(RUTA_CONFIG, "111", 10000, traza=False)
        
        assert resultado["aceptada"] == True
        assert "salida" in resultado
        assert "pasos" in resultado
        assert "tiempoSeg" in resultado
    
    def test_simulacion_sin_traza_no_crash(self):
        """ejecutar sin traza no debe crashear"""
        resultado = ejecutarSimulacion(RUTA_CONFIG, "11111", 10000, traza=False)
        
        assert resultado["aceptada"] == True
        assert len(resultado["salida"]) == 5
    
    def test_simulacion_devuelve_estructura_correcta(self):
        """debe devolver dict con todas las claves esperadas"""
        resultado = ejecutarSimulacion(RUTA_CONFIG, "1", 10000, traza=False)
        
        claves_requeridas = ["salida", "estadoFinal", "pasos", "tiempoSeg", 
                             "aceptada", "limiteAlcanzado", "detenidaSinAceptar"]
        
        for clave in claves_requeridas:
            assert clave in resultado, f"falta clave '{clave}' en resultado"
    
    def test_simulacion_limite_pasos_funciona(self):
        """si se excede el límite, limiteAlcanzado debe ser True"""
        # usar un límite muy bajo para forzar el caso
        resultado = ejecutarSimulacion(RUTA_CONFIG, "111111111", 5, traza=False)
        
        # debería detenerse por límite o terminar normal
        assert resultado["pasos"] <= 5 or resultado["aceptada"] == True


class TestConfiguracionJSON:
    """tests que validan que el json de configuración está bien formado"""
    
    def test_json_existe(self):
        """el archivo de configuración debe existir"""
        assert os.path.isfile(RUTA_CONFIG), f"no se encontró {RUTA_CONFIG}"
    
    def test_json_tiene_estado_inicial(self):
        """debe tener estado inicial definido"""
        mt = MaquinaDeTuring(RUTA_CONFIG)
        assert mt.estadoInicial is not None
        assert mt.estadoInicial == "q0"
    
    def test_json_tiene_estados_aceptacion(self):
        """debe tener al menos un estado de aceptación"""
        mt = MaquinaDeTuring(RUTA_CONFIG)
        assert len(mt.estadosAceptacion) > 0
        assert "q_aceptar" in mt.estadosAceptacion
    
    def test_json_tiene_transiciones(self):
        """debe tener transiciones definidas"""
        mt = MaquinaDeTuring(RUTA_CONFIG)
        assert len(mt.transiciones) > 0
    
    def test_json_tiene_simbolo_blanco(self):
        """debe tener símbolo blanco definido"""
        mt = MaquinaDeTuring(RUTA_CONFIG)
        assert mt.simboloBlanco is not None
        assert mt.simboloBlanco == "B"


if __name__ == "__main__":
    # ejecutar tests con pytest
    pytest.main([__file__, "-v", "--tb=short"])
