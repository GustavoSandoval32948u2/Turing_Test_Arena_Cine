
import random
import re
import unicodedata
from typing import Optional


class BancoPlantillas:
    """Banco de respuestas predeterminadas para el chatbot de cine."""

    TEMA_PREDETERMINADO = "el cine"

    PLANTILLAS = {
        "INICIO": [
            "¡Hola! ¿Qué película te gustaría comentar?",
            "¡Bienvenido al cine! ¿Qué historia te ha gustado últimamente?",
            "¡Buenas! ¿Prefieres las películas clásicas o modernas?",
            "¡Qué gusto! ¿Qué actor o actriz admiras?",
            "¡Hola! ¿Cuál es tu género cinematográfico favorito?",
            "¡Bienvenido! ¿Qué película recomendarías?",
        ],
        "SALUDANDO": [
            "¡Hola! ¿Qué película tienes en mente?",
            "¡Buenas! ¿Qué género cinematográfico prefieres?",
            "¡Qué gusto saludarte! ¿Qué has visto últimamente?",
            "¡Hola de nuevo! ¿Cuál es tu película favorita?",
            "¡Saludos! ¿Te gustan más las películas de acción o de drama?",
        ],
        "CONVERSANDO": [
            "¡Interesante! ¿Qué otra película recomendarías?",
            "¿Qué es lo que más disfrutas cuando ves una película?",
            "Si pudieras entrar en una película, ¿cuál elegirías?",
            "¿Qué actor te gustaría ver en una nueva película?",
            "¿Qué historia cinematográfica nunca olvidas?",
            "¿Prefieres un final inesperado o uno feliz?",
            "¿Qué película volverías a ver sin aburrirte?",
            "¡Hay mucho de qué hablar en el mundo del cine!",
            "¿Qué película consideras una obra maestra?",
            "¿Qué película te sorprendió más de lo esperado?",
            "¿Qué director de cine te parece interesante?",
        ],
        "HABLANDO_PELICULA": [
            "¡{tema}! ¿Qué escena recuerdas mejor?",
            "¿Qué personaje de {tema} te pareció más interesante?",
            "¿Le recomendarías {tema} a alguien? ¿Por qué?",
            "¿Qué cambiarías de la historia de {tema}?",
            "¿El final de {tema} te convenció?",
            "¿Qué puntuación le darías a {tema} del 1 al 10?",
            "¿Qué emoción te dejó {tema} al terminar?",
            "¿Volverías a ver {tema} dentro de unos años?",
            "¿Qué fue lo que más te gustó de {tema}?",
            "¿Qué aspecto de {tema} te pareció menos convincente?",
        ],
        "HABLANDO_ACTOR": [
            "¿Qué interpretación de {tema} te ha impresionado más?",
            "¿En qué película dirías que {tema} dio su mejor actuación?",
            "¿Te gustaría ver a {tema} en una película de terror?",
            "¿Qué personaje de {tema} recuerdas con más cariño?",
            "¿Cómo describirías el estilo actoral de {tema}?",
            "¿Con qué otro actor te gustaría ver a {tema} trabajar?",
            "¿Qué película de {tema} recomendarías primero?",
        ],
        "HABLANDO_GENERO": [
            "¿Qué película de {tema} recomendarías para una noche de cine?",
            "¿Qué elemento no puede faltar en una buena película de {tema}?",
            "¿Prefieres las películas clásicas o modernas de {tema}?",
            "¿Qué película de {tema} te sorprendió más?",
            "¿Qué hace que una película de {tema} sea excelente?",
            "¿Qué director relacionas con el género {tema}?",
        ],
        "OPINANDO": [
            "¡Interesante punto de vista! ¿Qué te hizo pensar así?",
            "No todo el mundo ve una película de la misma manera. ¿Qué detalle destacarías?",
            "¡Eso da para debatir! ¿Qué ejemplo cinematográfico se te ocurre?",
            "¿Crees que otras personas estarían de acuerdo contigo?",
            "¿Siempre has pensado así o cambiaste de opinión?",
            "¿Qué escena te hizo llegar a esa conclusión?",
        ],
        "PREGUNTANDO": [
            "¡Buena pregunta! ¿Te interesa más la historia o los personajes?",
            "Podemos verlo desde la dirección, el guion o la actuación. ¿Cuál prefieres?",
            "¡Vamos a hablar de cine! ¿Tienes alguna película concreta en mente?",
            "¿Quieres comparar películas o hablar de una en particular?",
            "¿Qué te llevó a preguntarte eso?",
            "¡Interesante! ¿Qué aspecto te gustaría explorar primero?",
        ],
        "PROVOCADO": [
            "¡Vaya, me estás poniendo a prueba! ¿Qué pista te hizo sospechar?",
            "¿Un bot? ¡Eso es justo lo que tendríamos que debatir! ¿Qué película nos pone a prueba?",
            "¡Buena provocación! ¿Qué tendría que decir para convencerte?",
            "¡No me declares culpable todavía! Hablemos de una película.",
            "¡Detective cinematográfico en acción! ¿Qué detalle te hizo sospechar?",
            "¿Crees que una buena conversación basta para distinguir a una máquina?",
            "¡Interesante acusación! ¿Qué actor interpretaría mejor a un robot?",
        ],
        "DESPEDIDA": [
            "¡Me gustó esta charla de cine! ¡Hasta la próxima película!",
            "¡Hasta luego! Que encuentres una película buenísima.",
            "¡Nos vemos en la próxima función!",
            "¡Gracias por la conversación! ¡Corte y fin!",
        ],
        "FINAL": [
            "La conversación ha terminado. ¡Hasta pronto!",
        ],
    }

    # Respuestas adaptadas al estado y al tipo de mensaje.
    RESPUESTAS_ESPECIFICAS = {
        ("CONVERSANDO", "MENCION_PELICULA"): [
            "¡{tema}! ¿Qué escena te impactó más?",
            "¿Qué nota le pondrías a {tema}?",
            "¿Qué hace especial a {tema} para ti?",
            "¿Recomendarías {tema}? ¿Por qué?",
        ],
        ("CONVERSANDO", "MENCION_ACTOR"): [
            "¿Cuál consideras la mejor actuación de {tema}?",
            "¿Qué película suya recomendarías primero?",
            "¿Con qué director te gustaría ver trabajar a {tema}?",
        ],
        ("CONVERSANDO", "MENCION_GENERO"): [
            "¿Qué película de {tema} nunca te cansas de ver?",
            "¿Qué característica define una buena película de {tema}?",
            "¿Qué película recomendarías para introducir a alguien en {tema}?",
        ],
        ("HABLANDO_PELICULA", "PREGUNTA"): [
            "Sobre {tema}, ¿qué escena recuerdas mejor?",
            "¿Qué escena de {tema} te impactó más?",
            "¿Qué personaje de {tema} te pareció más interesante?",
            "¿Qué opinas del final de {tema}?",
            "¿Qué momento de {tema} te pareció más emotivo?",
            "¿Qué cambiarías de la historia de {tema}?",
            "¿Qué parte de {tema} te gustaría analizar?",
            "¿Qué puntuación le darías a {tema} del 1 al 10?",
            "¿Qué mensaje crees que transmite {tema}?",
            "¿Volverías a ver {tema}? ¿Por qué?",
        ],
        ("HABLANDO_PELICULA", "OPINION"): [
            "¡Interesante opinión sobre {tema}! ¿Qué escena respalda tu punto de vista?",
            "¿Qué detalle de {tema} te llevó a esa conclusión?",
            "¿Crees que el final de {tema} fortalece su historia?",
            "¿Qué personaje de {tema} representa mejor esa idea?",
            "¿Qué cambiarías de {tema} para mejorarla?",
        ],
        ("HABLANDO_PELICULA", "AFIRMACION"): [
            "¡Entiendo! ¿Qué parte de {tema} te gusta más?",
            "¡Interesante! ¿Qué otra escena de {tema} destacarías?",
            "¿Qué personaje de {tema} te parece mejor desarrollado?",
        ],
        ("HABLANDO_PELICULA", "NEGACION"): [
            "Está bien. ¿Qué cambiarías de {tema}?",
            "Entiendo. ¿Qué película te parece mejor que {tema}?",
            "¿Qué aspecto de {tema} no terminó de convencerte?",
        ],
        ("HABLANDO_ACTOR", "PREGUNTA"): [
            "Sobre {tema}, ¿te interesa su mejor actuación o su trayectoria?",
            "¿En cuál película de {tema} te gustaría profundizar?",
            "¿Qué personaje interpretado por {tema} quieres comentar?",
        ],
        ("HABLANDO_ACTOR", "OPINION"): [
            "¿Qué actuación de {tema} respalda tu opinión?",
            "¿Crees que {tema} interpreta mejor el drama o la comedia?",
            "¿Qué película demuestra mejor el talento de {tema}?",
        ],
        ("HABLANDO_GENERO", "PREGUNTA"): [
            "Sobre el género {tema}, ¿quieres hablar de sus películas clásicas o modernas?",
            "¿Qué película de {tema} te gustaría analizar?",
            "¿Te interesa conocer películas de {tema} o comparar sus estilos?",
        ],
        ("HABLANDO_GENERO", "OPINION"): [
            "¿Qué película de {tema} representa mejor tu opinión?",
            "¿Qué característica de {tema} te gusta más?",
            "¿Qué película de {tema} recomendarías para defender esa idea?",
        ],
        ("OPINANDO", "PREGUNTA"): [
            "¿Qué aspecto de tu opinión te gustaría analizar?",
            "¿Podemos relacionar esa idea con alguna película?",
            "¿Qué ejemplo cinematográfico ayudaría a explicarlo?",
        ],
        ("PREGUNTANDO", "PREGUNTA"): [
            "¿Te interesa una respuesta sobre la historia, los actores o la dirección?",
            "¿Quieres analizar una película concreta o hablar de cine en general?",
            "¿Qué detalle te interesa conocer primero?",
        ],
    }

    # Respuestas generales según el token del clasificador.
    RESPUESTAS_TOKEN = {
        "PROVOCACION": [
            "¡Me estás poniendo a prueba! ¿Qué detalle te hizo sospechar?",
            "¡Buena acusación! ¿Cómo distinguirías a una persona de una máquina?",
            "¿Crees que una máquina podría mantener una conversación sobre cine?",
            "¡Interesante desafío! ¿Qué película trata mejor la inteligencia artificial?",
            "¡No saques conclusiones todavía! ¿Qué otra pregunta tienes para mí?",
        ],
        "PREGUNTA": [
            "¿Qué parte de ese tema te interesa más?",
            "¿Qué te hizo pensar en esa pregunta?",
            "¿Quieres que lo veamos desde otra perspectiva?",
            "¿Tienes algún ejemplo cinematográfico en mente?",
            "¿Qué respuesta te parecería más convincente?",
        ],
        "OPINION": [
            "¿Qué detalle te llevó a tener esa opinión?",
            "¿Qué otra película te ha provocado una impresión parecida?",
            "¿Crees que el director consiguió transmitir lo que quería?",
            "¿Tu opinión sería distinta si cambiaras el final?",
        ],
        "AFIRMACION": [
            "¡Entiendo! ¿Qué te gusta más de eso?",
            "¡De acuerdo! ¿Se te ocurre otro ejemplo?",
            "Interesante. ¿Siempre has pensado así?",
            "¡Perfecto! ¿Qué más añadirías?",
        ],
        "NEGACION": [
            "¡Está bien! ¿Qué opción prefieres entonces?",
            "Entiendo, no todas las películas son para todos. ¿Qué cambiarías?",
            "¡Vale! ¿Qué te convencería más?",
            "De acuerdo. ¿Qué alternativa recomendarías?",
        ],
        "RETOMAR_TEMA": [
            "¡Volvamos a ese tema! ¿Qué más puedes contarme?",
            "Retomemos la conversación. ¿Qué aspecto te interesa ahora?",
        ],
        "DESCONOCIDO": [
            "¡Cuéntame un poco más!",
            "¿Cómo se relaciona eso con el cine?",
            "¡Eso me da curiosidad! ¿Puedes explicarlo de otra forma?",
            "¿Qué otra cosa te gustaría comentar?",
        ],
    }

    def __init__(self, semilla: Optional[int] = None):
        self._aleatorio = random.Random(semilla)
        self._ultima_respuesta = {}

    def obtener(
        self,
        estado,
        pila=None,
        token="DESCONOCIDO",
        entidad=None,
    ):
        """
        Obtiene una respuesta sin cambiar la interfaz pública del proyecto.

        Prioridad:
        1. Provocación.
        2. Despedida.
        3. Respuesta específica para estado y token.
        4. Respuesta general para token.
        5. Plantilla del estado.
        6. Respuesta de respaldo.
        """
        estado = self._normalizar(estado)
        token = self._normalizar(token)
        tema = self._obtener_tema(pila, entidad)

        if token == "PROVOCACION":
            opciones = self.RESPUESTAS_TOKEN["PROVOCACION"]

        elif token == "DESPEDIDA":
            opciones = self.PLANTILLAS["DESPEDIDA"]

        elif (estado, token) in self.RESPUESTAS_ESPECIFICAS:
            opciones = self.RESPUESTAS_ESPECIFICAS[(estado, token)]

        elif token in self.RESPUESTAS_TOKEN:
            opciones = self.RESPUESTAS_TOKEN[token]

        else:
            opciones = self.PLANTILLAS.get(
                estado,
                self.RESPUESTAS_TOKEN["DESCONOCIDO"],
            )

        if not opciones:
            opciones = self.RESPUESTAS_TOKEN["DESCONOCIDO"]

        # Evita repetir inmediatamente la misma respuesta
        # para una combinación de estado y token.
        clave = (estado, token)
        anterior = self._ultima_respuesta.get(clave)
        disponibles = [r for r in opciones if r != anterior]

        if not disponibles:
            disponibles = opciones

        plantilla = self._aleatorio.choice(disponibles)

        try:
            respuesta = plantilla.format(tema=tema)
        except (KeyError, ValueError, IndexError, AttributeError):
            respuesta = self._respuesta_segura(tema)

        self._ultima_respuesta[clave] = plantilla

        respuesta = re.sub(r"\s+", " ", respuesta).strip()

        return respuesta or self._respuesta_segura(tema)

    @staticmethod
    def _normalizar(valor):
        """Normaliza etiquetas sin modificar el texto de la conversación."""
        if not isinstance(valor, str):
            return ""

        return valor.strip().upper()

    @classmethod
    def _obtener_tema(cls, pila=None, entidad=None):
        """
        Prioriza la entidad detectada en el mensaje.
        Si no existe, intenta recuperar el tema de la pila.
        """
        if isinstance(entidad, str) and entidad.strip():
            return cls._limpiar_tema(entidad)

        if pila is not None:
            try:
                tema = pila.peek()

                if isinstance(tema, str) and tema.strip():
                    return cls._limpiar_tema(tema)

            except (AttributeError, IndexError, KeyError, TypeError):
                pass

        return cls.TEMA_PREDETERMINADO

    @staticmethod
    def _limpiar_tema(tema):
        if not isinstance(tema, str):
            return "el cine"

        tema = re.sub(r"\s+", " ", tema).strip()
        return tema or "el cine"

    @staticmethod
    def _respuesta_segura(tema="el cine"):
        return (
            f"¡Interesante! Hablemos de {tema}. "
            "¿Qué es lo que más te llama la atención?"
        )

    @classmethod
    def estados_disponibles(cls):
        return tuple(cls.PLANTILLAS.keys())

    @classmethod
    def validar_plantillas(cls):
        """Comprueba el formato de todas las plantillas."""
        errores = []

        grupos = [
            ("PLANTILLAS", cls.PLANTILLAS),
            ("RESPUESTAS_TOKEN", cls.RESPUESTAS_TOKEN),
            ("RESPUESTAS_ESPECIFICAS", cls.RESPUESTAS_ESPECIFICAS),
        ]

        for nombre_grupo, grupo in grupos:
            for clave, opciones in grupo.items():
                if not isinstance(opciones, list) or not opciones:
                    errores.append(
                        f"{nombre_grupo}, {clave}: "
                        "debe contener una lista no vacía."
                    )
                    continue

                for numero, plantilla in enumerate(opciones, start=1):
                    if not isinstance(plantilla, str):
                        errores.append(
                            f"{nombre_grupo}, {clave}, "
                            f"respuesta {numero}: no es texto."
                        )
                        continue

                    try:
                        plantilla.format(tema="Tema de prueba")
                    except (KeyError, ValueError, IndexError) as error:
                        errores.append(
                            f"{nombre_grupo}, {clave}, "
                            f"respuesta {numero}: {error}"
                        )

        return errores

    def reiniciar(self):
        """Permite limpiar el historial de respuestas repetidas."""
        self._ultima_respuesta.clear()


if __name__ == "__main__":
    banco = BancoPlantillas(semilla=42)

    errores = banco.validar_plantillas()

    if errores:
        print("ERROR: se encontraron problemas en las plantillas:")

        for error in errores:
            print("-", error)
    else:
        print("PASS: todas las plantillas son válidas.")

    print("\nPruebas de respuestas:")

    pruebas = [
        ("HABLANDO_PELICULA", "PREGUNTA", "Titanic"),
        ("HABLANDO_PELICULA", "OPINION", "Titanic"),
        ("HABLANDO_ACTOR", "PREGUNTA", "Leonardo DiCaprio"),
        ("HABLANDO_GENERO", "PREGUNTA", "terror"),
        ("CONVERSANDO", "PROVOCACION", None),
        ("CONVERSANDO", "DESCONOCIDO", None),
        ("CONVERSANDO", "DESPEDIDA", None),
    ]

    for estado, token, entidad in pruebas:
        respuesta = banco.obtener(
            estado=estado,
            token=token,
            entidad=entidad,
        )

        print(f"[{estado} / {token}] {respuesta}")

    print("\nPrueba de contexto:")

    class PilaPrueba:
        def peek(self):
            return "Titanic"

    print(
        banco.obtener(
            estado="HABLANDO_PELICULA",
            pila=PilaPrueba(),
            token="PREGUNTA",
        )
    )
