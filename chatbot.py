
import random
import re
import unicodedata

from definiciones import ESTADO_INICIAL
from afd.clasificador import ClasificadorAFD
from afn.dialogo import MotorAFN
from pila.contexto import PilaContexto
from plantillas.banco import BancoPlantillas


class ChatbotCine:
    """Chatbot de cine basado en AFD, AFN, pila y plantillas."""

    ESTADOS_TEMATICOS = {
        "HABLANDO_PELICULA",
        "HABLANDO_ACTOR",
        "HABLANDO_GENERO",
    }

    TOKENS_TEMATICOS = {
        "MENCION_PELICULA": "HABLANDO_PELICULA",
        "MENCION_ACTOR": "HABLANDO_ACTOR",
        "MENCION_GENERO": "HABLANDO_GENERO",
    }

    # ==========================================
    # BANCO DE CONOCIMIENTOS: PELICULAS
    # ==========================================

    PELICULAS = {
        "titanic": {
            "nombre": "Titanic",
            "argumento": (
                "Titanic combina un romance ficticio con el "
                "hundimiento real del transatlántico en 1912. "
                "La historia utiliza la relación entre Jack y Rose "
                "para mostrar las diferencias sociales y la tragedia "
                "del naufragio."
            ),
            "escena": (
                "Una de las escenas más recordadas es cuando Jack "
                "y Rose están en la proa del barco. También destaca "
                "la secuencia del hundimiento."
            ),
            "final": (
                "El final muestra a Rose sobreviviendo y llegando "
                "a una edad avanzada. Jack muere durante el "
                "naufragio, y Rose termina arrojando el diamante "
                "al océano."
            ),
            "personajes": (
                "Los personajes principales son Jack Dawson, "
                "Rose DeWitt Bukater, Cal Hockley y Molly Brown. "
                "Jack y Rose representan el contraste entre "
                "las clases sociales."
            ),
            "reparto": (
                "Leonardo DiCaprio interpreta a Jack y Kate Winslet "
                "interpreta a Rose. También participan Billy Zane "
                "como Cal y Kathy Bates como Molly Brown."
            ),
            "opinion": (
                "Titanic combina romance, drama y una tragedia "
                "histórica de manera emotiva. Sus actuaciones "
                "y su música son especialmente memorables."
            ),
            "opinion_final": (
                "En mi opinión, el final de Titanic es emotivo "
                "y trágico. Rose sobrevive, pero la muerte de Jack "
                "deja una pérdida profunda. El diamante refuerza "
                "la importancia de los recuerdos."
            ),
            "significado_final": (
                "El final representa la memoria, la pérdida "
                "y la libertad personal. Rose conserva la historia "
                "de Jack y demuestra que aquella experiencia "
                "transformó su vida."
            ),
        },

        "inception": {
            "nombre": "Inception",
            "argumento": (
                "Inception sigue a un especialista que entra "
                "en los sueños de otras personas para extraer "
                "información. Su misión consiste en implantar "
                "una idea, lo que complica los límites entre "
                "sueño, memoria y realidad."
            ),
            "escena": (
                "Una de las escenas más llamativas es aquella "
                "en la que la ciudad parece doblarse sobre sí misma. "
                "También destacan las secuencias de sueños "
                "dentro de otros sueños."
            ),
            "final": (
                "Al final, Cobb regresa con sus hijos y hace girar "
                "su tótem. La película termina antes de mostrar "
                "con certeza si el objeto cae o continúa girando."
            ),
            "personajes": (
                "Los personajes principales son Dom Cobb, Arthur, "
                "Ariadne, Eames, Mal y Saito. Cada uno cumple "
                "una función importante en la misión."
            ),
            "reparto": (
                "Leonardo DiCaprio interpreta a Cobb, "
                "Joseph Gordon-Levitt a Arthur, Elliot Page "
                "a Ariadne, Tom Hardy a Eames y Ken Watanabe "
                "a Saito. Marion Cotillard interpreta a Mal."
            ),
            "opinion": (
                "Inception destaca por su estructura narrativa, "
                "sus efectos visuales y sus preguntas sobre "
                "la realidad y los sueños."
            ),
            "opinion_final": (
                "En mi opinión, el final de Inception funciona "
                "porque deja al espectador con la duda de si "
                "Cobb está soñando. Esa ambigüedad hace que "
                "el desenlace siga siendo interesante."
            ),
            "significado_final": (
                "El final deja abierta la duda de si Cobb está "
                "soñando. Una interpretación es que el tótem "
                "ya no es lo más importante para él: decide "
                "centrarse en el reencuentro con sus hijos."
            ),
        },

        "matrix": {
            "nombre": "The Matrix",
            "argumento": (
                "The Matrix presenta un mundo en el que "
                "la humanidad vive conectada a una realidad "
                "simulada creada por máquinas. Neo descubre "
                "la verdad y se une a una resistencia."
            ),
            "escena": (
                "Una de las escenas más famosas es cuando Neo "
                "esquiva las balas. También destaca su elección "
                "entre la píldora roja y la azul."
            ),
            "final": (
                "Neo comprende mejor sus capacidades dentro "
                "de Matrix y logra enfrentarse a los agentes. "
                "El final anticipa su intención de liberar "
                "a otras personas del sistema."
            ),
            "personajes": (
                "Los personajes principales son Neo, Morfeo, "
                "Trinity, el agente Smith y el Oráculo."
            ),
            "reparto": (
                "Keanu Reeves interpreta a Neo, Laurence Fishburne "
                "a Morfeo, Carrie-Anne Moss a Trinity y Hugo Weaving "
                "al agente Smith."
            ),
            "opinion": (
                "The Matrix combina acción, ciencia ficción "
                "y reflexiones filosóficas sobre la realidad "
                "y la libertad."
            ),
            "opinion_final": (
                "El final resulta satisfactorio porque muestra "
                "la transformación de Neo y abre posibilidades "
                "para continuar la historia."
            ),
            "significado_final": (
                "El desenlace simboliza el despertar de Neo "
                "y su capacidad de cuestionar las reglas "
                "de una realidad aparentemente inalterable."
            ),
        },

        "avatar": {
            "nombre": "Avatar",
            "argumento": (
                "Avatar cuenta la historia de Jake Sully, "
                "un exmarine que llega a Pandora y utiliza "
                "un cuerpo avatar para relacionarse con "
                "los habitantes del planeta."
            ),
            "escena": (
                "Destacan los vuelos sobre Pandora y las "
                "secuencias que muestran sus paisajes "
                "y criaturas extraordinarias."
            ),
            "final": (
                "Jake decide permanecer con los Na'vi "
                "y transfiere definitivamente su conciencia "
                "a su cuerpo avatar."
            ),
            "personajes": (
                "Los personajes principales son Jake Sully, "
                "Neytiri, Grace Augustine y el coronel Quaritch."
            ),
            "reparto": (
                "Sam Worthington interpreta a Jake Sully, "
                "Zoe Saldaña a Neytiri, Sigourney Weaver "
                "a Grace y Stephen Lang a Quaritch."
            ),
            "opinion": (
                "Avatar destaca por su mundo visual, "
                "sus efectos especiales y sus temas "
                "sobre la naturaleza y el colonialismo."
            ),
            "opinion_final": (
                "El final es esperanzador porque Jake "
                "encuentra una nueva comunidad y decide "
                "defender el mundo que ahora considera su hogar."
            ),
            "significado_final": (
                "El final representa una transformación "
                "de identidad y una elección de pertenencia "
                "y respeto por la naturaleza."
            ),
        },

        "oppenheimer": {
            "nombre": "Oppenheimer",
            "argumento": (
                "Oppenheimer narra la vida del físico "
                "J. Robert Oppenheimer y su participación "
                "en el desarrollo de la bomba atómica "
                "durante la Segunda Guerra Mundial."
            ),
            "escena": (
                "Una de las secuencias más impactantes "
                "es la prueba Trinity, que muestra "
                "el poder destructivo de la nueva arma."
            ),
            "final": (
                "La película termina destacando las "
                "consecuencias morales y políticas "
                "de la creación de las armas nucleares."
            ),
            "personajes": (
                "Los personajes centrales incluyen "
                "a J. Robert Oppenheimer, Lewis Strauss, "
                "Kitty Oppenheimer y Leslie Groves."
            ),
            "reparto": (
                "Cillian Murphy interpreta a Oppenheimer, "
                "Robert Downey Jr. a Lewis Strauss, "
                "Emily Blunt a Kitty y Matt Damon "
                "a Leslie Groves."
            ),
            "opinion": (
                "Oppenheimer destaca por sus actuaciones, "
                "su montaje y la reflexión sobre "
                "la responsabilidad científica."
            ),
            "opinion_final": (
                "El desenlace es inquietante porque "
                "presenta las consecuencias de un avance "
                "científico que cambió la historia."
            ),
            "significado_final": (
                "El final plantea que los descubrimientos "
                "científicos pueden producir consecuencias "
                "que sus creadores no pueden controlar."
            ),
        },

        "barbie": {
            "nombre": "Barbie",
            "argumento": (
                "Barbie sigue a una muñeca que comienza "
                "a cuestionar su vida aparentemente perfecta "
                "y viaja al mundo real para comprender "
                "su identidad."
            ),
            "escena": (
                "Destacan las secuencias musicales "
                "de Barbieland y el contraste visual "
                "entre ese mundo y la realidad."
            ),
            "final": (
                "Barbie decide abandonar su existencia "
                "como muñeca y comenzar una vida humana "
                "con nuevas posibilidades."
            ),
            "personajes": (
                "Los personajes principales son Barbie, "
                "Ken, Gloria, Sasha y la Barbie Rara."
            ),
            "reparto": (
                "Margot Robbie interpreta a Barbie, "
                "Ryan Gosling a Ken, America Ferrera "
                "a Gloria y Ariana Greenblatt a Sasha."
            ),
            "opinion": (
                "Barbie combina humor, fantasía "
                "y crítica social con una estética "
                "muy reconocible."
            ),
            "opinion_final": (
                "El final es positivo porque Barbie "
                "elige construir su propia identidad."
            ),
            "significado_final": (
                "El desenlace representa la libertad "
                "de elegir quién queremos ser, "
                "sin depender de expectativas externas."
            ),
        },
    }

    # ==========================================
    # ACTORES
    # ==========================================

    ACTORES = {
        "leonardo dicaprio": {
            "nombre": "Leonardo DiCaprio",
            "descripcion": (
                "Leonardo DiCaprio es un actor conocido "
                "por interpretar personajes complejos "
                "y por colaborar con Martin Scorsese."
            ),
            "peliculas": (
                "Titanic, Inception, El renacido, "
                "El lobo de Wall Street y Atrápame si puedes."
            ),
        },
        "brad pitt": {
            "nombre": "Brad Pitt",
            "descripcion": (
                "Brad Pitt es un actor reconocido "
                "por su versatilidad en dramas, "
                "comedias y películas de acción."
            ),
            "peliculas": (
                "El club de la pelea, Seven, "
                "Troya y Érase una vez en Hollywood."
            ),
        },
        "tom hanks": {
            "nombre": "Tom Hanks",
            "descripcion": (
                "Tom Hanks es conocido por sus "
                "interpretaciones en películas "
                "dramáticas y familiares."
            ),
            "peliculas": (
                "Forrest Gump, Náufrago, "
                "Rescatando al soldado Ryan y Toy Story."
            ),
        },
        "tom cruise": {
            "nombre": "Tom Cruise",
            "descripcion": (
                "Tom Cruise es reconocido por sus "
                "películas de acción y por realizar "
                "numerosas escenas de riesgo."
            ),
            "peliculas": (
                "Misión imposible, Top Gun, "
                "Minority Report y Al filo del mañana."
            ),
        },
        "keanu reeves": {
            "nombre": "Keanu Reeves",
            "descripcion": (
                "Keanu Reeves es conocido por sus "
                "papeles en películas de acción "
                "y ciencia ficción."
            ),
            "peliculas": (
                "The Matrix, John Wick, "
                "Constantine y Máxima velocidad."
            ),
        },
        "cillian murphy": {
            "nombre": "Cillian Murphy",
            "descripcion": (
                "Cillian Murphy es un actor reconocido "
                "por sus interpretaciones intensas "
                "en cine y televisión."
            ),
            "peliculas": (
                "Oppenheimer, Inception, "
                "28 días después y Dunkerque."
            ),
        },
        "margot robbie": {
            "nombre": "Margot Robbie",
            "descripcion": (
                "Margot Robbie es una actriz conocida "
                "por su versatilidad y sus papeles "
                "en comedias y dramas."
            ),
            "peliculas": (
                "Barbie, El lobo de Wall Street, "
                "Yo, Tonya y Escuadrón suicida."
            ),
        },
    }

    # ==========================================
    # GENEROS
    # ==========================================

    RESPUESTAS_GENERO = {
        "terror": (
            "El terror busca provocar miedo, inquietud "
            "o tensión. Puede apoyarse en criaturas, "
            "atmósferas, suspense o temores psicológicos."
        ),
        "accion": (
            "La acción destaca por sus persecuciones, "
            "combates, conflictos y escenas de gran energía."
        ),
        "comedia": (
            "La comedia utiliza situaciones, diálogos "
            "y personajes para provocar humor."
        ),
        "drama": (
            "El drama se centra en conflictos humanos, "
            "emociones y decisiones importantes."
        ),
        "romance": (
            "El romance desarrolla relaciones afectivas "
            "y conflictos sentimentales entre personajes."
        ),
        "ciencia ficcion": (
            "La ciencia ficción explora tecnologías, "
            "mundos futuros y preguntas sobre "
            "la ciencia y la humanidad."
        ),
        "animacion": (
            "La animación permite contar historias "
            "mediante técnicas visuales muy variadas, "
            "desde aventuras hasta dramas."
        ),
    }

    ALIAS_PELICULAS = {
        "titanic": "titanic",
        "inception": "inception",
        "el origen": "inception",
        "matrix": "matrix",
        "the matrix": "matrix",
        "avatar": "avatar",
        "oppenheimer": "oppenheimer",
        "barbie": "barbie",
    }

    ALIAS_ACTORES = {
        "leonardo dicaprio": "leonardo dicaprio",
        "dicaprio": "leonardo dicaprio",
        "brad pitt": "brad pitt",
        "tom hanks": "tom hanks",
        "tom cruise": "tom cruise",
        "keanu reeves": "keanu reeves",
        "cillian murphy": "cillian murphy",
        "margot robbie": "margot robbie",
    }

    ALIAS_GENEROS = {
        "terror": "terror",
        "accion": "accion",
        "comedia": "comedia",
        "drama": "drama",
        "romance": "romance",
        "ciencia ficcion": "ciencia ficcion",
        "animacion": "animacion",
    }

    RECOMENDACIONES = [
        "Si buscas ciencia ficción, te recomiendo Inception o The Matrix.",
        "Si prefieres drama histórico, puedes ver Titanic u Oppenheimer.",
        "Si buscas fantasía y aventura, Avatar es una buena opción.",
        "Si quieres una comedia con crítica social, puedes probar Barbie.",
    ]

    # ==========================================
    # INICIALIZACION
    # ==========================================

    def __init__(self, semilla=None):
        self.semilla = semilla
        self.estado_actual = ESTADO_INICIAL
        self.estado_contexto = None

        self.aleatorio = random.Random(semilla)

        self.clasificador = ClasificadorAFD()
        self.afn = MotorAFN(semilla=semilla)
        self.pila = PilaContexto()
        self.plantillas = BancoPlantillas(semilla)

        self.historial_tipos = []

    # ==========================================
    # UTILIDADES
    # ==========================================

    @staticmethod
    def _normalizar_texto(texto):
        texto = unicodedata.normalize(
            "NFD", str(texto).lower()
        )

        texto = "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )

        texto = re.sub(
            r"[¿?¡!,.;:()\"']",
            " ",
            texto
        )

        return " ".join(texto.split())

    @classmethod
    def _contiene(cls, texto, frases):
        texto = cls._normalizar_texto(texto)

        for frase in frases:
            frase = cls._normalizar_texto(frase)

            if re.search(
                r"(?<!\w)" + re.escape(frase) + r"(?!\w)",
                texto
            ):
                return True

        return False

    @classmethod
    def _es_pregunta(cls, texto):
        if "?" in texto or "¿" in texto:
            return True

        t = cls._normalizar_texto(texto)

        return t.startswith((
            "que ", "quien ", "quienes ",
            "cual ", "cuales ", "como ",
            "cuando ", "donde ", "por que ",
            "dime ", "explica ", "describe ",
        ))

    @classmethod
    def _buscar_alias(cls, texto, alias):
        t = cls._normalizar_texto(texto)

        coincidencias = []

        for nombre, identificador in alias.items():
            nombre_normalizado = cls._normalizar_texto(nombre)

            encontrado = re.search(
                r"(?<!\w)"
                + re.escape(nombre_normalizado)
                + r"(?!\w)",
                t
            )

            if encontrado:
                coincidencias.append((
                    encontrado.start(),
                    -len(nombre_normalizado),
                    identificador
                ))

        if not coincidencias:
            return None

        coincidencias.sort()
        return coincidencias[0][2]

    def _tema_actual(self):
        return self.pila.peek()

    def _tipo_tema_actual(self):
        if self.historial_tipos:
            return self.historial_tipos[-1]

        return None

    def _pelicula_conocida(self, tema, texto):
        identificador = self._buscar_alias(
            texto, self.ALIAS_PELICULAS
        )

        if identificador:
            return self.PELICULAS.get(identificador)

        identificador = self._buscar_alias(
            tema or "", self.ALIAS_PELICULAS
        )

        return self.PELICULAS.get(identificador)

    def _actor_conocido(self, tema, texto):
        identificador = self._buscar_alias(
            texto, self.ALIAS_ACTORES
        )

        if identificador:
            return self.ACTORES.get(identificador)

        identificador = self._buscar_alias(
            tema or "", self.ALIAS_ACTORES
        )

        return self.ACTORES.get(identificador)

    def _genero_conocido(self, tema, texto):
        identificador = self._buscar_alias(
            texto, self.ALIAS_GENEROS
        )

        if identificador:
            return identificador

        return self._buscar_alias(
            tema or "", self.ALIAS_GENEROS
        )

    def _nombre_canonico(self, token, texto, entidad):
        if token == "MENCION_PELICULA":
            pelicula = self._pelicula_conocida(None, texto)

            if pelicula:
                return pelicula["nombre"]

        if token == "MENCION_ACTOR":
            actor = self._actor_conocido(None, texto)

            if actor:
                return actor["nombre"]

        if token == "MENCION_GENERO":
            genero = self._genero_conocido(None, texto)

            if genero:
                return genero

        return None

    # ==========================================
    # MANEJO DE PILA
    # ==========================================

    def _guardar_tema(self, tema, tipo):
        if not tema or not tipo:
            return

        if (
            self._tema_actual() == tema
            and self._tipo_tema_actual() == tipo
        ):
            return

        self.pila.push(tema)
        self.historial_tipos.append(tipo)

    def _retomar_tema(self):
        if len(self.historial_tipos) <= 1:
            return

        self.pila.pop()
        self.historial_tipos.pop()

    # ==========================================
    # DETECCION DE INTENCIONES
    # ==========================================

    def _detectar_intencion(self, texto):
        t = self._normalizar_texto(texto)

        if self._contiene(t, (
            "que significa el final",
            "que significa el desenlace",
            "que quiere decir el final",
            "cual es el significado del final",
            "como se interpreta el final",
            "que representa el final",
            "que simboliza el final",
            "interpretacion del final",
        )):
            return "significado_final"

        if self._contiene(t, (
            "que opinas del final",
            "que piensas del final",
            "que te parece el final",
            "tu opinion del final",
            "que opinas del desenlace",
            "que piensas del desenlace",
        )):
            return "opinion_final"

        if self._contiene(t, (
            "recomienda",
            "recomiendame",
            "recomiendas",
            "recomendar",
            "recomendacion",
            "recomendaciones",
            "que pelicula veo",
            "que pelicula me recomiendas",
            "sugiere una pelicula",
            "sugerencia de pelicula",
        )):
            return "recomendacion"

        if self._contiene(t, (
            "parecida a",
            "similar a",
            "comparada con",
            "diferencia entre",
            "compara",
            "cual es mejor",
            "que pelicula es mejor",
            "cual pelicula es mejor",
            "que es mejor",
        )):
            return "comparacion"

        if self._contiene(t, (
            "que significa",
            "que quiere decir",
            "que simboliza",
            "mensaje de la pelicula",
            "interpretacion",
        )):
            return "significado"

        if self._contiene(t, (
            "que opinas",
            "que piensas",
            "que te parece",
            "tu opinion",
            "tu punto de vista",
            "te gusta",
            "es buena",
            "es malo",
            "es mala",
            "vale la pena",
            "merece la pena",
        )):
            return "opinion"

        if self._contiene(t, (
            "actor", "actores",
            "actriz", "actrices",
            "director", "directora",
            "quien interpreta",
            "quien actua",
            "elenco", "reparto",
        )):
            return "reparto"

        if self._contiene(t, (
            "personaje", "personajes",
            "protagonista", "protagonistas",
            "quienes son",
            "quien aparece",
            "quienes aparecen",
        )):
            return "personajes"

        if self._contiene(t, (
            "de que trata",
            "de que va",
            "argumento",
            "sinopsis",
            "resumen",
            "historia de",
        )):
            return "argumento"

        if self._contiene(t, (
            "escena",
            "momento",
            "parte de la pelicula",
            "parte de la historia",
        )):
            return "escena"

        if self._contiene(t, (
            "como termina",
            "como termino",
            "como acaba",
            "que pasa al final",
            "que ocurre al final",
            "final",
            "desenlace",
        )):
            return "final"

        if self._contiene(t, (
            "me gusto",
            "me gusta",
            "me encanto",
            "me encanta",
            "me parecio buena",
            "estuvo buena",
            "me aburrio",
            "no me gusto",
            "no me gusta",
            "me parecio mala",
            "estuvo mala",
        )):
            return "reaccion"

        if self._es_pregunta(texto):
            return "pregunta_general"

        return "comentario"

    # ==========================================
    # RESPUESTAS SOBRE PELICULAS
    # ==========================================

    def _responder_sobre_pelicula(
        self, pelicula, intencion, texto
    ):
        nombre = pelicula["nombre"]

        campos = {
            "argumento": "argumento",
            "escena": "escena",
            "final": "final",
            "personajes": "personajes",
            "reparto": "reparto",
            "opinion": "opinion",
            "opinion_final": "opinion_final",
            "significado_final": "significado_final",
        }

        if intencion in campos:
            campo = campos[intencion]
            return pelicula.get(campo, pelicula["argumento"])

        if intencion == "significado":
            return pelicula.get(
                "significado_final",
                pelicula["opinion"]
            )

        if intencion == "reaccion":
            return (
                f"Es interesante conocer tu impresión de {nombre}. "
                "¿Qué fue lo que más te gustó "
                "o te llamó la atención?"
            )

        if intencion == "pregunta_general":
            return (
                f"Sobre {nombre}, puedo explicarte su argumento, "
                "personajes, escenas importantes, reparto o final. "
                "¿Qué detalle te interesa conocer?"
            )

        respuestas = [
            (
                f"¡Buena elección! {nombre} tiene varios aspectos "
                "que podemos analizar. ¿Por dónde comenzamos?"
            ),
            (
                f"¡{nombre}! Es una película interesante "
                "para comentar. ¿Qué te gustaría saber "
                "de su historia?"
            ),
        ]

        return self.aleatorio.choice(respuestas)

    # ==========================================
    # RESPUESTAS SOBRE ACTORES
    # ==========================================

    def _responder_actor(self, actor, intencion, texto):
        nombre = actor["nombre"]

        if self._contiene(texto, (
            "que peliculas",
            "cuales peliculas",
            "peliculas ha hecho",
            "peliculas hizo",
            "filmografia",
            "en que peliculas",
        )):
            return (
                f"Entre sus películas más conocidas están "
                f"{actor['peliculas']}"
            )

        if intencion == "opinion":
            return (
                f"Me parece que {nombre} destaca por "
                "sus interpretaciones y su capacidad "
                "para adaptarse a distintos personajes."
            )

        if intencion == "reparto":
            return (
                f"{nombre} ha participado en películas como "
                f"{actor['peliculas']}"
            )

        return (
            f"¡{nombre}! {actor['descripcion']} "
            "¿Qué película suya recuerdas mejor?"
        )

    # ==========================================
    # RESPUESTAS SOBRE GENEROS
    # ==========================================

    def _responder_genero(self, texto, tema):
        genero = self._genero_conocido(tema, texto)

        if genero:
            return self.RESPUESTAS_GENERO[genero]

        return (
            "Podemos hablar de terror, acción, comedia, "
            "drama, romance, ciencia ficción o animación. "
            "¿Qué género prefieres?"
        )

    # ==========================================
    # RESPUESTAS DEL BANCO DE PLANTILLAS
    # ==========================================

    def _respuesta_plantilla(self, token, tema=None):
        return self.plantillas.obtener(
            self.estado_actual,
            pila=self.pila,
            token=token,
            entidad=tema
        )

    # ==========================================
    # SELECCION DE RESPUESTA
    # ==========================================

    def _responder_directamente(self, texto, tema, token):
        intencion = self._detectar_intencion(texto)

        print(f"[INTENCION] {intencion}")

        token = (
            token.strip().upper()
            if isinstance(token, str)
            else "DESCONOCIDO"
        )

        # Despedidas, saludos y provocaciones

        if token == "DESPEDIDA":
            return self._respuesta_plantilla(
                "DESPEDIDA", tema
            )

        if token == "PROVOCACION":
            return self._respuesta_plantilla(
                "PROVOCACION", tema
            )

        if token == "SALUDO":
            return self._respuesta_plantilla(
                "SALUDO", tema
            )

        # Recuperar tema anterior

        if token == "RETOMAR_TEMA":
            if tema:
                return (
                    f"¡Claro! Volvamos a {tema}. "
                    "¿Qué te gustaría comentar sobre ese tema?"
                )

            return (
                "Todavía no tenemos un tema anterior "
                "para retomar. ¿De qué película quieres hablar?"
            )

        # Afirmaciones

        if token == "AFIRMACION":
            if tema:
                return (
                    f"¡Entiendo! Entonces seguimos con {tema}. "
                    "¿Qué otro aspecto te gustaría comentar?"
                )

            return (
                "¡Perfecto! ¿De qué película, actor "
                "o género quieres hablar?"
            )

        # Negaciones

        if token == "NEGACION":
            if tema:
                return (
                    "Está bien, podemos cambiar de tema "
                    f"o explorar otro aspecto de {tema}. "
                    "¿Qué prefieres?"
                )

            return (
                "No hay problema. Podemos hablar "
                "de otra película o género."
            )

        # Recomendaciones generales

        if intencion == "recomendacion":
            return self.aleatorio.choice(
                self.RECOMENDACIONES
            )

        # Comparaciones generales

        if intencion == "comparacion":
            return (
                "Podemos comparar dos películas por su argumento, "
                "personajes, dirección y desenlace. "
                "¿Qué dos películas quieres comparar?"
            )

        # Películas desconocidas

        if (
            self._contiene(texto, (
                "hablemos de",
                "hablar de",
            ))
            and self._contiene(texto, (
                "pelicula",
                "peliculas",
            ))
            and self._pelicula_conocida(None, texto) is None
        ):
            return (
                "No tengo información específica sobre esa película. "
                "Podemos hablar de Titanic, Inception, The Matrix, "
                "Avatar, Oppenheimer o Barbie. "
                "¿Cuál prefieres?"
            )

        # Identificar tipo de contexto

        tipo = self._tipo_tema_actual()

        if token in self.TOKENS_TEMATICOS:
            tipo = self.TOKENS_TEMATICOS[token]

        # Actores

        if tipo == "HABLANDO_ACTOR":
            actor = self._actor_conocido(tema, texto)

            if actor:
                return self._responder_actor(
                    actor, intencion, texto
                )

            if tema:
                return (
                    f"Podemos hablar de {tema}. "
                    "¿Qué película o interpretación "
                    "te gustaría comentar?"
                )

        # Géneros

        if tipo == "HABLANDO_GENERO":
            genero = self._genero_conocido(tema, texto)

            if intencion == "opinion" and genero:
                return (
                    f"Me parece que el género {genero} "
                    "puede ofrecer historias interesantes "
                    "cuando combina buenos personajes, "
                    "un ritmo adecuado y una propuesta original. "
                    f"¿Qué es lo que más te gusta del {genero}?"
                )

            return self._responder_genero(texto, tema)

        # Películas

        if tipo == "HABLANDO_PELICULA":
            pelicula = self._pelicula_conocida(
                tema, texto
            )

            if pelicula:
                return self._responder_sobre_pelicula(
                    pelicula, intencion, texto
                )

            if tema:
                return (
                    f"Podemos seguir hablando de {tema}. "
                    "¿Te interesa su historia, "
                    "los personajes o alguna escena?"
                )

        # Película explícita

        pelicula = self._pelicula_conocida(None, texto)

        if pelicula:
            return self._responder_sobre_pelicula(
                pelicula, intencion, texto
            )

        # Actor explícito

        actor = self._actor_conocido(None, texto)

        if actor:
            return self._responder_actor(
                actor, intencion, texto
            )

        # Género explícito

        genero = self._genero_conocido(None, texto)

        if genero:
            return self._responder_genero(texto, genero)

        # Opiniones generales

        if intencion == "opinion":
            return (
                "Para valorar una película, considero importantes "
                "la historia, el desarrollo de los personajes "
                "y la forma en que transmite sus emociones. "
                "Los efectos visuales ayudan, pero no sustituyen "
                "una historia sólida."
            )

        # Reacciones

        if intencion == "reaccion":
            if tema:
                return (
                    f"Es interesante conocer tu impresión de {tema}. "
                    "¿Qué fue lo que más te gustó "
                    "o te llamó la atención?"
                )

            return (
                "Cada persona vive las películas de manera diferente. "
                "¿Qué fue lo que más te llamó la atención?"
            )

        # Respuesta general del banco

        return self._respuesta_plantilla(token, tema)

    # ==========================================
    # PROCESAMIENTO PRINCIPAL
    # ==========================================

    def procesar_entrada(self, texto_usuario):
        if (
            not isinstance(texto_usuario, str)
            or not texto_usuario.strip()
        ):
            return "Escribe algo para que podamos hablar de cine."

        texto_usuario = texto_usuario.strip()

        # 1. Clasificación mediante el AFD

        resultado = self.clasificador.clasificar_detallado(
            texto_usuario
        )

        token = resultado.token
        entidad = resultado.entidad

        # 2. Interpretación complementaria

        intencion = self._detectar_intencion(
            texto_usuario
        )

        if self._contiene(texto_usuario, (
            "eres un bot",
            "eres humano",
            "no pareces humano",
            "pareces un robot",
            "eres una maquina",
            "eres inteligencia artificial",
        )):
            token = "PROVOCACION"
            entidad = None

        elif token == "MENCION_PELICULA":
            pelicula = self._pelicula_conocida(
                None, texto_usuario
            )

            if pelicula is None:
                if intencion in (
                    "recomendacion",
                    "comparacion",
                ):
                    token = "PREGUNTA"
                else:
                    token = "DESCONOCIDO"

                entidad = None

        # Mantener preguntas generales sin crear temas falsos

        if (
            token == "DESCONOCIDO"
            and intencion in (
                "recomendacion",
                "comparacion",
            )
        ):
            token = "PREGUNTA"

        print(f"[AFD] Token: {token}")

        if entidad:
            print(f"[AFD] Entidad: {entidad}")

        # 3. Identificar nuevo tema

        tipo_nuevo = self.TOKENS_TEMATICOS.get(
            token
        )

        tema_nuevo = None

        if tipo_nuevo:
            tema_nuevo = self._nombre_canonico(
                token, texto_usuario, entidad
            )

        # 4. Recuperar el estado temático anterior

        estado_retorno = None

        if (
            token == "RETOMAR_TEMA"
            and len(self.historial_tipos) > 1
        ):
            estado_retorno = self.historial_tipos[-2]

        # 5. Transición mediante el AFN

        estado_anterior = self.estado_actual

        nuevo_estado, acciones = self.afn.transicionar(
            estado_anterior,
            token,
            entidad,
            estado_retorno=estado_retorno
        )

        self.estado_actual = nuevo_estado

        # 6. Ejecutar acciones de pila

        for accion in acciones:
            tipo_accion = accion.get("tipo")

            if tipo_accion == "push":
                if tema_nuevo and tipo_nuevo:
                    self._guardar_tema(
                        tema_nuevo, tipo_nuevo
                    )

            elif tipo_accion == "pop":
                self._retomar_tema()

        # Garantizar el registro del nuevo tema

        if tema_nuevo and tipo_nuevo:
            self._guardar_tema(
                tema_nuevo, tipo_nuevo
            )

        # 7. Obtener contexto actual

        tema = self._tema_actual()
        tipo_contexto = self._tipo_tema_actual()

        self.estado_contexto = tipo_contexto

        # 8. Generar respuesta

        respuesta = self._responder_directamente(
            texto_usuario,
            tema,
            token
        )

        # 9. Mostrar información de depuración

        print(
            f"[CHATBOT] {estado_anterior} "
            f"-> {self.estado_actual}"
        )

        print(
            f"[CHATBOT] Tema actual: "
            f"{tema or 'ninguno'}"
        )

        print(
            f"[CHATBOT] Contexto: "
            f"{self.estado_contexto or 'ninguno'}"
        )

        print(f"[RESPUESTA] Token: {token}")

        return respuesta

    # ==========================================
    # CONSULTAS DE ESTADO
    # ==========================================

    def obtener_estado(self):
        return self.estado_actual

    def obtener_contexto(self):
        return {
            "estado": self.estado_actual,
            "estado_contexto": self.estado_contexto,
            "tema": self._tema_actual(),
            "cantidad_temas": len(self.historial_tipos),
        }

    # ==========================================
    # REINICIO
    # ==========================================

    def reiniciar(self):
        self.estado_actual = ESTADO_INICIAL
        self.estado_contexto = None

        self.pila = PilaContexto()
        self.historial_tipos.clear()

        self.afn.reiniciar()

        self.plantillas = BancoPlantillas(
            self.semilla
        )

        self.aleatorio = random.Random(
            self.semilla
        )

    # ==========================================
    # HISTORIAL DEL AFN
    # ==========================================

    def obtener_historial_afn(self):
        return self.afn.obtener_historial()


# ==============================================
# EJECUCION DESDE TERMINAL
# ==============================================

if __name__ == "__main__":
    bot = ChatbotCine(semilla=42)

    print("\nCINEBOT - Chatbot de Cine")
    print("Escribe 'salir' para terminar.\n")

    while True:
        try:
            mensaje = input("\nTÚ: ").strip()

            if mensaje.lower() == "salir":
                break

            if not mensaje:
                continue

            respuesta = bot.procesar_entrada(
                mensaje
            )

            print(f"CINEBOT: {respuesta}")

        except (KeyboardInterrupt, EOFError):
            print("\nCerrando CineBot...")
            break
