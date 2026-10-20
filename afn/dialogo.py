
# ============================================
# MOTOR AFN - DIALOGO DEL CHATBOT DE CINE
# Proyecto: Turing Test Arena
# ============================================

import random

from definiciones import ESTADO_INICIAL, TRANSICIONES


class MotorAFN:
    """
    Motor de dialogo no determinista.

    Selecciona aleatoriamente uno de los estados destino
    permitidos para el estado actual y el token recibido.

    Tambien propone acciones para la pila de contexto.
    """

    def __init__(self, semilla=None):
        self.aleatorio = random.Random(semilla)
        self.historial_transiciones = []

    def transicionar(
            self,
            estado_actual,
            token,
            entidad=None,
            estado_retorno=None,
        ):
        """
        Devuelve:
            (nuevo_estado, acciones_pila)

        acciones_pila es una lista de diccionarios.
        """

        estado_actual = (
            estado_actual
            if isinstance(estado_actual, str)
            else ESTADO_INICIAL
        )

        token = (
            token.strip().upper()
            if isinstance(token, str)
            else "DESCONOCIDO"
        )

        # Buscar los destinos definidos para esta combinacion.
        destinos = TRANSICIONES.get(
            (estado_actual, token), []
        )

        # Eliminar destinos duplicados y vacios.
        destinos = list(dict.fromkeys(
            destino for destino in destinos
            if isinstance(destino, str) and destino.strip()
        ))

        if token == "RETOMAR_TEMA" and estado_retorno in (
            "HABLANDO_PELICULA",
            "HABLANDO_ACTOR",
            "HABLANDO_GENERO",
        ):
            destinos = [estado_retorno]
            nuevo_estado = estado_retorno
            motivo = "recuperacion de contexto"

        elif destinos:
            nuevo_estado = self.aleatorio.choice(destinos)
            motivo = "transicion definida"

        else:
            nuevo_estado = estado_actual
            motivo = "sin transicion definida"

        acciones_pila = []

        if token in (
            "MENCION_PELICULA",
            "MENCION_ACTOR",
            "MENCION_GENERO",
        ) and isinstance(entidad, str) and entidad.strip():
            acciones_pila.append({
                "tipo": "push",
                "valor": entidad.strip()
            })

        elif token == "RETOMAR_TEMA":
            acciones_pila.append({
                "tipo": "pop"
            })

        self.historial_transiciones.append({
            "origen": estado_actual,
            "token": token,
            "destino": nuevo_estado,
            "opciones": destinos.copy(),
            "motivo": motivo
        })

        print(
            f"[AFN] {estado_actual} --{token}--> "
            f"{nuevo_estado}"
        )

        if len(destinos) > 1:
            print(f"[AFN] Opciones disponibles: {destinos}")
            print(f"[AFN] Seleccion aleatoria: {nuevo_estado}")

        return nuevo_estado, acciones_pila

    def reiniciar(self):
        """Limpia el historial de transiciones."""
        self.historial_transiciones.clear()

    def obtener_historial(self):
        """Devuelve una copia del historial de transiciones."""
        return self.historial_transiciones.copy()
