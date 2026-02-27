"""
Carga la definición desde JSON y ejecuta paso a paso.
Cinta conceptualmente infinita (se expande dinámicamente).
"""

from __future__ import annotations
import json
from typing import List, Dict, Optional


class MaquinaDeTuring:

    def __init__(self, archivoJson: str):
        self.estados: List[str] = []
        self.alfabetoEntrada: List[str] = []
        self.alfabetoCinta: List[str] = []
        self.estadoInicial: Optional[str] = None
        self.estadosAceptacion: List[str] = []
        self.simboloBlanco: str = "_"
        self.transiciones: List[Dict[str, str]] = []
        self.cinta: List[str] = []
        self.posicionCabeza: int = 0
        self.estadoActual: Optional[str] = None
        self.pasosEjecutados: int = 0
        self.cargarMaquina(archivoJson)

    def cargarMaquina(self, archivoJson: str) -> None:
        """Lee el JSON y carga los componentes de la MT."""
        with open(archivoJson, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.estados = datos.get("states", [])
        self.alfabetoEntrada = datos.get("input_alphabet", [])
        self.alfabetoCinta = datos.get("tape_alphabet", [])
        self.estadoInicial = datos.get("initial_state")
        self.estadosAceptacion = datos.get("accept_states", [])
        self.simboloBlanco = datos.get("blank_symbol", "_")
        self.transiciones = datos.get("transitions", [])

    def inicializarCinta(self, cadenaEntrada: str) -> None:
        """Coloca la cadena en la cinta y reinicia cabeza/estado/contador."""
        self.cinta = list(cadenaEntrada) if cadenaEntrada else []
        if not self.cinta:
            self.cinta.append(self.simboloBlanco)
        self.posicionCabeza = 0
        self.estadoActual = self.estadoInicial
        self.pasosEjecutados = 0

    def buscarTransicion(self, estado: str, simbolo: str) -> Optional[Dict[str, str]]:
        """Primera transición que coincida con (estado, símbolo)."""
        for t in self.transiciones:
            if t.get("current_state") == estado and t.get("read_symbol") == simbolo:
                return t
        return None

    def ejecutarPaso(self) -> bool:
        """Ejecuta un paso. Devuelve False si no puede avanzar."""
        if self.estadoActual is None or self.estadoActual in self.estadosAceptacion:
            return False

        if self.posicionCabeza < 0:
            self.cinta = [self.simboloBlanco] * (-self.posicionCabeza) + self.cinta
            self.posicionCabeza = 0
        if self.posicionCabeza >= len(self.cinta):
            self.cinta.append(self.simboloBlanco)

        simboloActual = self.cinta[self.posicionCabeza]
        transicion = self.buscarTransicion(self.estadoActual, simboloActual)
        if transicion is None:
            return False

        self.cinta[self.posicionCabeza] = transicion.get("write_symbol", simboloActual)
        movimiento = transicion.get("move", "N")

        if movimiento == "L":
            self.posicionCabeza -= 1
        elif movimiento == "R":
            self.posicionCabeza += 1

        if self.posicionCabeza < 0:
            self.cinta.insert(0, self.simboloBlanco)
            self.posicionCabeza = 0
        elif self.posicionCabeza >= len(self.cinta):
            self.cinta.append(self.simboloBlanco)

        self.estadoActual = transicion.get("next_state", self.estadoActual)
        self.pasosEjecutados += 1
        return True

    def ejecutar(self, cadenaEntrada: str, maxPasos: int = 10000) -> str:
        """Ejecuta completa y devuelve el contenido útil de la cinta."""
        self.inicializarCinta(cadenaEntrada)
        for _ in range(maxPasos):
            if self.estadoActual in self.estadosAceptacion:
                break
            if not self.ejecutarPaso():
                break
        return self.obtenerContenidoCinta()

    def obtenerContenidoCinta(self) -> str:
        """Devuelve los símbolos no-blanco de la cinta."""
        if not self.cinta:
            return ""
        primero = ultimo = None
        for i, sim in enumerate(self.cinta):
            if sim != self.simboloBlanco:
                if primero is None:
                    primero = i
                ultimo = i
        if primero is None:
            return ""
        return "".join(self.cinta[primero : ultimo + 1])
