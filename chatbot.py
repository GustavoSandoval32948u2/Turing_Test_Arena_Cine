
# ============================================
# CHATBOT PRINCIPAL - INTEGRACION
# Responsable: Gustavo Sandoval
# Tema: Cine
# ============================================

import random

from definiciones import ESTADO_INICIAL, TRANSICIONES
from afd.clasificador import ClasificadorAFD
from pila.contexto import PilaContexto
from plantillas.banco import BancoPlantillas


class ChatbotCine:
    def __init__(self, semilla=None):
        self.estado_actual = ESTADO_INICIAL

        self.clasificador = ClasificadorAFD()
        self.pila = PilaContexto()
        self.plantillas = BancoPlantillas(semilla)

        self.aleatorio = random.Random(semilla)

        print("Chatbot de Cine - Arquitectura lista")
        print(f"Estado inicial: {self.estado_actual}")
        print("-" * 50)

    def procesar_entrada(self, texto_usuario: str) -> str:
        # 1. Clasificacion lexica mediante el AFD
        resultado = self.clasificador.clasificar_detallado(
            texto_usuario
        )
        token = resultado.token
        entidad = resultado.entidad

        print(f"[AFD] Token: {token}")
        if entidad:
            print(f"[AFD] Entidad detectada: {entidad}")

        # 2. Transicion provisional basada en las definiciones.
        # Se sustituira por MotorAFN cuando Gencer entregue el modulo.
        estado_anterior = self.estado_actual
        posibles = TRANSICIONES.get(
            (estado_anterior, token), []
        )

        if posibles:
            nuevo_estado = self.aleatorio.choice(posibles)
        elif token == "DESPEDIDA":
            nuevo_estado = "DESPEDIDA"
        elif token == "SALUDO":
            nuevo_estado = "SALUDANDO"
        elif token.startswith("MENCION_"):
            nuevo_estado = {
                "MENCION_PELICULA": "HABLANDO_PELICULA",
                "MENCION_ACTOR": "HABLANDO_ACTOR",
                "MENCION_GENERO": "HABLANDO_GENERO",
            }.get(token, "CONVERSANDO")
        elif token == "OPINION":
            nuevo_estado = "OPINANDO"
        elif token == "PREGUNTA":
            nuevo_estado = "PREGUNTANDO"
        elif token == "PROVOCACION":
            nuevo_estado = "PROVOCADO"
        else:
            nuevo_estado = "CONVERSANDO"

        self.estado_actual = nuevo_estado
        print(
            f"[DIALOGO PROVISIONAL] "
            f"{estado_anterior} -> {self.estado_actual}"
        )

        # 3. Actualizacion de la pila de contexto
        if token in (
            "MENCION_PELICULA",
            "MENCION_ACTOR",
            "MENCION_GENERO",
        ) and entidad:
            tema_actual = self.pila.peek()

            if tema_actual != entidad:
                self.pila.push(entidad)

        elif token == "RETOMAR_TEMA":
            entidad = self.pila.peek()

        # 4. Generacion de respuesta
        respuesta = self.plantillas.obtener(
            self.estado_actual,
            self.pila,
            token=token,
            entidad=entidad,
        )

        return respuesta
