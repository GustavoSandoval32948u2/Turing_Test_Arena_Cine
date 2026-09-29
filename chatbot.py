# ============================================
# CHATBOT PRINCIPAL - INTEGRACIÓN
# Responsable: Gustavo Sandoval
# Tema: Cine
# ============================================

from definiciones import ESTADO_INICIAL

# Estas importaciones las usarán tus compañeros cuando entreguen su código
# from afd.clasificador import ClasificadorAFD
# from afn.dialogo import MotorAFN
# from pila.contexto import PilaContexto
# from plantillas.banco import BancoPlantillas

class ChatbotCine:
    def __init__(self):
        self.estado_actual = ESTADO_INICIAL
        
        # Aquí se conectarán los módulos de tus compañeros:
        # self.clasificador = ClasificadorAFD()
        # self.motor_afn = MotorAFN()
        # self.pila = PilaContexto()
        # self.plantillas = BancoPlantillas()

        print("Chatbot de Cine - Arquitectura lista")
        print(f"Estado inicial: {self.estado_actual}")
        print("-" * 50)

    def procesar_entrada(self, texto_usuario: str) -> str:
        """
        Flujo oficial del sistema (esto es lo que debes poder explicar):
        
        1. texto_usuario
        2. → AFD (clasificación) → token
        3. → AFN (transición) → nuevo estado
        4. → Pila (push / pop / peek)
        5. → Banco de plantillas → respuesta
        """
        
        # --- 1. Clasificación léxica (Edin) ---
        # token = self.clasificador.clasificar(texto_usuario)
        token = "DESCONOCIDO"  # temporal hasta que Edin entregue

        # --- 2. Transición de estado (Gencer) ---
        # nuevo_estado, acciones_pila = self.motor_afn.transicionar(self.estado_actual, token)
        # self.estado_actual = nuevo_estado
        nuevo_estado = self.estado_actual  # temporal

        # --- 3. Actualizar pila (Gencer) ---
        # for accion in acciones_pila:
        #     if accion["tipo"] == "push":
        #         self.pila.push(accion["valor"])
        #     elif accion["tipo"] == "pop":
        #         self.pila.pop()

        # --- 4. Generar respuesta (Daniel) ---
        # respuesta = self.plantillas.obtener(self.estado_actual, self.pila)
        respuesta = f"[Estado actual: {self.estado_actual}] Respuesta temporal"

        return respuesta