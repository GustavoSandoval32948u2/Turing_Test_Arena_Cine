
import random
import re
from typing import Optional


class BancoPlantillas:
    """
    Banco de respuestas predeterminadas para el chatbot de cine.

    Responsabilidades:
    - Guardar respuestas organizadas por estado.
    - Seleccionar respuestas de forma aleatoria.
    - Personalizar respuestas con películas, actores y géneros.
    - Recuperar el tema actual desde la pila de contexto.
    - Evitar respuestas vacías o errores de formato.
    - Facilitar pruebas y futuras integraciones con el AFN.

    No utiliza inteligencia artificial generativa.
    """

    TEMA_PREDETERMINADO = "ese tema"

    PLANTILLAS = {
        "INICIO": [
            "¡Hola! Me gusta conversar sobre cine. ¿Qué película te interesa?",
            "¡Bienvenido! Podemos hablar de películas, actores y géneros.",
            "¡Hola! ¿Tienes alguna película favorita?",
            "¡Qué gusto tenerte aquí! ¿Qué te gustaría conversar sobre cine?",
        ],

        "SALUDANDO": [
            "¡Hola! ¿Qué tipo de películas te gustan?",
            "¡Qué gusto saludarte! ¿Hablamos de cine?",
            "¡Buenas! ¿Tienes alguna película favorita?",
            "¡Hola de nuevo! ¿Qué película tienes en mente?",
        ],

        "CONVERSANDO": [
            "Interesante. Cuéntame un poco más.",
            "¿Y qué opinas tú sobre ese tema?",
            "Podemos seguir hablando de cine. ¿Qué tienes en mente?",
            "Eso da para una buena conversación. ¿Qué más me cuentas?",
            "¡Qué interesante! ¿Hay algo más que te gustaría comentar?",
            "Me gustaría conocer tu punto de vista. ¿Qué piensas al respecto?",
        ],

        "HABLANDO_PELICULA": [
            "¡{tema}! ¿Qué es lo que más te gusta de esa película?",
            "¿Qué destacarías de {tema}? ¿La recomendarías?",
            "¿Qué te parece la historia de {tema}?",
            "¿Volverías a ver {tema} o prefieres descubrir otra película?",
            "¿Qué destacarías más de {tema}?",
            "¿Qué personaje de {tema} te parece más interesante?",
            "¿Qué sensación te dejó {tema} después de verla?",
            "Si pudieras cambiar algo de {tema}, ¿qué sería?",
        ],

        "HABLANDO_ACTOR": [
            "¿Qué actuación de {tema} te ha gustado más?",
            "¿Qué te parece el estilo de actuación de {tema}?",
            "¿En qué película recuerdas más a {tema}?",
            "¿Crees que {tema} encaja bien en los papeles que interpreta?",
            "¿Qué personaje interpretado por {tema} destacarías?",
            "¿Te gustaría ver a {tema} en algún otro género cinematográfico?",
        ],

        "HABLANDO_GENERO": [
            "¿Qué película de {tema} recomendarías?",
            "¿Qué es lo que más disfrutas del género {tema}?",
            "¿Prefieres las películas clásicas o las más recientes de {tema}?",
            "¿Qué hace que una película de {tema} sea buena para ti?",
            "¿Cuál es tu película favorita del género {tema}?",
            "¿Qué elemento no puede faltar en una buena película de {tema}?",
        ],

        "OPINANDO": [
            "Interesante opinión. ¿Qué te hace pensar eso?",
            "Entiendo tu punto de vista. ¿Qué otro aspecto destacarías?",
            "Cada persona puede interpretar una película de forma diferente. ¿Por qué opinas así?",
            "¿Crees que esa opinión cambiaría si vieras la película otra vez?",
            "Es interesante conocer distintas perspectivas. ¿Qué más piensas?",
        ],

        "PREGUNTANDO": [
            "Buena pregunta. ¿Qué aspecto del cine te interesa más?",
            "Podemos hablar de la historia, los personajes o las actuaciones. ¿Por dónde empezamos?",
            "Me interesa lo que preguntas. ¿Qué te hizo pensar en eso?",
            "¿Quieres que hablemos de una película, un actor o un género en particular?",
            "Podemos explorar ese tema desde diferentes puntos de vista. ¿Qué te interesa saber?",
        ],

        "PROVOCADO": [
            "¡Vaya! Podemos tener opiniones diferentes. ¿Seguimos hablando de cine?",
            "No pasa nada, cada quien tiene su forma de pensar. ¿Qué película prefieres?",
            "¡Defendamos nuestras opiniones! ¿Qué te parece una buena película?",
            "Podemos debatir sin problema. ¿Qué película defenderías a capa y espada?",
        ],

        "DESPEDIDA": [
            "¡Ha sido una buena conversación sobre cine! ¡Hasta pronto!",
            "¡Hasta luego! Que encuentres una gran película para ver.",
            "¡Nos vemos! Cuando quieras, seguimos hablando de cine.",
            "¡Gracias por conversar conmigo! ¡Hasta la próxima!",
        ],

        "FINAL": [
            "La conversación ha terminado. ¡Hasta pronto!",
        ],
    }

    # Respuestas especiales cuando el estado general es CONVERSANDO,
    # pero el AFD detecta un tema específico.
    RESPUESTAS_ESPECIFICAS = {
        ("CONVERSANDO", "MENCION_PELICULA"): [
            "¡{tema}! ¿Qué te parece esa película?",
            "¿Qué es lo que más recuerdas de {tema}?",
            "¿Recomendarías {tema} a tus amigos?",
        ],

        ("CONVERSANDO", "MENCION_ACTOR"): [
            "¿Qué actuación de {tema} destacarías?",
            "¿En qué película recuerdas a {tema}?",
            "¿Qué te parece el trabajo de {tema} en el cine?",
        ],

        ("CONVERSANDO", "MENCION_GENERO"): [
            "¿Qué película de {tema} te gusta más?",
            "¿Qué es lo que más disfrutas del género {tema}?",
            "¿Qué película recomendarías para alguien que disfruta de {tema}?",
        ],
    }

    def __init__(self, semilla: Optional[int] = None):
        """
        semilla:
            Permite reproducir la selección aleatoria durante las pruebas.
            Si se omite, la selección es aleatoria normalmente.
        """
        self._aleatorio = random.Random(semilla)

    def obtener(
        self,
        estado,
        pila=None,
        token="DESCONOCIDO",
        entidad=None
    ):
        """
        Devuelve una respuesta para el estado actual.

        estado:
            Estado del AFN, por ejemplo HABLANDO_PELICULA.

        pila:
            Instancia de PilaContexto. Se utiliza como respaldo
            cuando no se proporciona una entidad.

        token:
            Token léxico devuelto por el AFD.

        entidad:
            Película, actor o género detectado por el clasificador.

        Devuelve:
            Una cadena de texto lista para mostrar al usuario.
        """

        estado = self._normalizar_estado(estado)
        token = self._normalizar_token(token)
        tema = self._limpiar_tema(
            self._obtener_tema(pila, entidad)
        )

        opciones = self.RESPUESTAS_ESPECIFICAS.get(
            (estado, token)
        )

        if not opciones:
            opciones = self.PLANTILLAS.get(estado)

        if not opciones:
            opciones = self.PLANTILLAS["CONVERSANDO"]

        plantilla = self._aleatorio.choice(opciones)

        try:
            respuesta = plantilla.format(tema=tema)
        except (KeyError, ValueError, IndexError):
            # Evita que una plantilla mal formada detenga el chatbot.
            respuesta = self.PLANTILLAS["CONVERSANDO"][0]

        respuesta = respuesta.strip()

        if not respuesta:
            return self.PLANTILLAS["CONVERSANDO"][0]

        return respuesta

    @staticmethod
    def _normalizar_estado(estado):
        """Convierte el estado a una cadena segura."""
        if not isinstance(estado, str):
            return ""

        return estado.strip().upper()

    @staticmethod
    def _normalizar_token(token):
        """Convierte el token a una cadena segura."""
        if not isinstance(token, str):
            return "DESCONOCIDO"

        return token.strip().upper() or "DESCONOCIDO"

    @classmethod
    def _obtener_tema(cls, pila=None, entidad=None):
        """
        Prioridad:
        1. Entidad detectada en la entrada actual.
        2. Tema guardado en la pila.
        3. Tema genérico.
        """
        if entidad is not None:
            tema = cls._limpiar_tema(entidad)
            if tema:
                return tema

        if pila is not None:
            try:
                tema = cls._limpiar_tema(pila.peek())
                if tema:
                    return tema
            except (AttributeError, IndexError):
                # La pila todavía podría no tener el método peek
                # o podría no estar disponible.
                pass

        return cls.TEMA_PREDETERMINADO

    @classmethod
    def _limpiar_tema(cls, tema):
        """Evita insertar valores vacíos o saltos de línea en respuestas."""
        if not isinstance(tema, str):
            return ""

        tema = re.sub(r"\s+", " ", tema).strip()
        return tema

    @classmethod
    def estados_disponibles(cls):
        """Devuelve los estados que tienen plantillas."""
        return tuple(cls.PLANTILLAS.keys())

    @classmethod
    def validar_plantillas(cls):
        """
        Revisa que existan respuestas para todos los estados
        definidos y que las plantillas tengan formato válido.

        Devuelve una lista de errores.
        Una lista vacía significa que no se detectaron problemas.
        """
        errores = []

        try:
            from definiciones import ESTADOS
        except ImportError:
            ESTADOS = list(cls.PLANTILLAS.keys())

        for estado in ESTADOS:
            opciones = cls.PLANTILLAS.get(estado)

            if not opciones:
                errores.append(
                    f"El estado {estado} no tiene plantillas."
                )
                continue

            for numero, plantilla in enumerate(opciones, start=1):
                if not isinstance(plantilla, str) or not plantilla.strip():
                    errores.append(
                        f"Plantilla vacía o inválida: {estado}, opción {numero}."
                    )
                    continue

                try:
                    plantilla.format(tema="Tema de prueba")
                except (KeyError, ValueError, IndexError) as error:
                    errores.append(
                        f"Error de formato en {estado}, opción "
                        f"{numero}: {error}"
                    )

        for clave, opciones in cls.RESPUESTAS_ESPECIFICAS.items():
            for numero, plantilla in enumerate(opciones, start=1):
                try:
                    plantilla.format(tema="Tema de prueba")
                except (KeyError, ValueError, IndexError) as error:
                    errores.append(
                        f"Error de formato en respuesta específica "
                        f"{clave}, opción {numero}: {error}"
                    )

        return errores


if __name__ == "__main__":
    banco = BancoPlantillas()

    print("Validando banco de respuestas...")
    errores = banco.validar_plantillas()

    if errores:
        print("Se encontraron problemas:")
        for error in errores:
            print(f"- {error}")
    else:
        print("PASS: todas las plantillas son válidas.")

    print("\nEjemplos de respuestas:")
    print("Película:", banco.obtener(
        "HABLANDO_PELICULA",
        token="MENCION_PELICULA",
        entidad="Titanic"
    ))
    print("Actor:", banco.obtener(
        "HABLANDO_ACTOR",
        token="MENCION_ACTOR",
        entidad="Tom Hanks"
    ))
    print("Género:", banco.obtener(
        "HABLANDO_GENERO",
        token="MENCION_GENERO",
        entidad="comedia"
    ))
