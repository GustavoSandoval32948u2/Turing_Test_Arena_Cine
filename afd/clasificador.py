
import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from definiciones import TOKENS


@dataclass(frozen=True)
class ResultadoLexico:
    """Resultado detallado de una clasificacion para pruebas y defensa."""
    entrada_original: str
    entrada_normalizada: str
    palabras: Tuple[str, ...]
    token: str
    estado_final: str
    regla: str
    coincidencia: Optional[str] = None
    entidad: Optional[str] = None
    automata: Optional[str] = None
    recorrido: Tuple[Tuple[int, str, int], ...] = ()


class ClasificadorAFD:
    """Banco de AFD de frases, con seleccion determinista por prioridad.

    Cada AFD consume toda la secuencia mediante su tabla delta total.
    Los estados q0..qn cuentan el prefijo reconocido; qn es absorbente.
    Los nombres q_<token> son etiquetas de salida, no estados internos.
    """

    # Frases/palabras generales. Se escriben sin tildes porque la entrada se
    # normaliza antes de comparar.
    REGLAS: Dict[str, Tuple[str, ...]] = {
        "SALUDO": (
            "hola", "buenas", "buenos dias", "buenas tardes", "buenas noches",
            "que tal", "hey", "holi", "saludos"
        ),
        "DESPEDIDA": (
            "adios", "hasta luego", "hasta pronto", "nos vemos", "chao", "chau",
            "me voy", "bye", "hasta manana"
        ),
        "AFIRMACION": (
            "si", "claro", "correcto", "exacto", "de acuerdo", "por supuesto",
            "totalmente", "asi es", "tambien"
        ),
        "NEGACION": (
            "no", "nunca", "jamas", "para nada", "no creo", "negativo"
        ),
        "OPINION": (
            # Palabras del diagrama: me gusta, odio, prefiero, la mejor.
            "me gusta", "odio", "prefiero", "la mejor",
            "me encanta", "me fascina", "me parece", "creo que",
            "pienso que", "opino", "para mi", "considero", "es buena", "es mala",
            "es genial", "es aburrida", "es excelente", "es terrible"
        ),
        "RETOMAR_TEMA": (
            "volvamos", "regresemos", "retomemos", "sigamos con", "sobre lo anterior",
            "de lo anterior", "ese tema", "esa pelicula", "el tema anterior"
        ),
        "PROVOCACION": (
            # Palabras del diagrama: aburrido, malo, idiota, no sabes, eres tonto.
            "aburrido", "malo", "idiota", "no sabes", "eres tonto",
            # Ampliacion para la prueba acordada; no figuraba en el diagrama original.
            "eres un bot",
            "estupido", "tonto", "inutil", "callate", "basura",
            "no sirves", "eres malo", "que aburrido eres"
        ),
    }

    PALABRAS_PREGUNTA = (
        "que", "quien", "quienes", "cual", "cuales", "como", "cuando", "donde",
        "por que", "porque", "cuanto", "cuantos", "cuanta", "cuantas"
    )

    # Catalogos pequenos y editables para reconocer entidades del dominio.
    PELICULAS: Tuple[str, ...] = (
        "titanic", "avatar", "oppenheimer", "barbie", "inception", "interestelar",
        "interstellar", "matrix", "gladiador", "el padrino", "pulp fiction",
        "jurassic park", "toy story", "star wars", "harry potter", "parasitos",
        "joker", "batman", "dune", "duna", "shrek", "coco", "cars",
        "el senor de los anillos", "forrest gump", "la la land"
    )

    # Disparadores genéricos mostrados en el diagrama. Se evalúan como respaldo
    # para no desplazar una PREGUNTA u OPINION más específica.
    INDICADORES_PELICULA: Tuple[str, ...] = (
        "pelicula", "filme", "movie", "peli"
    )

    ACTORES: Tuple[str, ...] = (
        "leonardo dicaprio", "brad pitt", "tom hanks", "tom cruise", "johnny depp",
        "robert downey jr", "scarlett johansson", "margot robbie", "emma stone",
        "zendaya", "timothee chalamet", "cillian murphy", "keanu reeves",
        "christian bale", "joaquin phoenix", "morgan freeman"
    )

    INDICADORES_ACTOR: Tuple[str, ...] = (
        "actor", "actriz", "protagonista", "dirigida por"
    )

    GENEROS: Tuple[str, ...] = (
        "accion", "aventura", "comedia", "drama", "terror", "horror", "suspenso",
        "ciencia ficcion", "fantasia", "romance", "animacion", "documental",
        "musical", "western", "crimen", "misterio", "thriller"
    )

    # La prioridad es parte de la definicion determinista del clasificador.
    # Entidades van antes de PREGUNTA para conservar el tema de cine, por ejemplo:
    # "Que opinas de Titanic?" -> MENCION_PELICULA.
    PRIORIDAD: Tuple[str, ...] = (
        "PROVOCACION",
        "DESPEDIDA",
        "SALUDO",
        "RETOMAR_TEMA",
        "MENCION_PELICULA",
        "MENCION_ACTOR",
        "MENCION_GENERO",
        "OPINION",
        "NEGACION",
        "AFIRMACION",
        "PREGUNTA",
    )

    def __init__(self):
        self.automatas = []
        for token in self.PRIORIDAD:
            opciones = {
                "MENCION_PELICULA": self.PELICULAS,
                "MENCION_ACTOR": self.ACTORES,
                "MENCION_GENERO": self.GENEROS,
                "PREGUNTA": ("?", "¿") + self.PALABRAS_PREGUNTA,
            }.get(token, self.REGLAS.get(token, ()))
            # Orden estable: prioridad de categoria y frase mas larga.
            if token != "PREGUNTA":
                opciones = sorted(opciones, key=len, reverse=True)
            for frase in opciones:
                self.automatas.append(AFDFrase(token, frase))
        for token, frases in (("MENCION_PELICULA", self.INDICADORES_PELICULA),
                              ("MENCION_ACTOR", self.INDICADORES_ACTOR)):
            for frase in sorted(frases, key=len, reverse=True):
                self.automatas.append(AFDFrase(token, frase))
        for i, afd in enumerate(self.automatas):
            afd.nombre = f"A{i:03d}"

    def normalizar(self, texto: str) -> str:
        texto = unicodedata.normalize("NFD", (texto or "").lower())
        texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
        texto = "".join(c if c in "abcdefghijklmnopqrstuvwxyz0123456789¿?¡!" else " "
                        for c in texto)
        return " ".join(texto.split())

    def simbolos(self, texto: str) -> Tuple[str, ...]:
        texto = self.normalizar(texto)
        for signo in "¿?¡!":
            texto = texto.replace(signo, f" {signo} ")
        return tuple(texto.split())

    def tokenizar(self, texto: str) -> List[str]:
        return [s for s in self.simbolos(texto) if s not in "¿?¡!"]

    def clasificar_detallado(self, texto: str) -> ResultadoLexico:
        original = texto or ""
        normalizado = self.normalizar(original)
        palabras = tuple(self.tokenizar(original))
        simbolos = self.simbolos(original)
        # Solo signos o espacios se consideran entrada sin contenido lexico.
        if palabras:
            for afd in self.automatas:
                estado, pasos = afd.ejecutar(simbolos)
                if estado == afd.final:
                    return ResultadoLexico(
                        original, normalizado, palabras, afd.token,
                        f"{afd.nombre}:q{estado}",
                        f"AFD {afd.nombre} acepta la frase {afd.frase!r}",
                        afd.frase,
                        afd.frase if afd.token.startswith("MENCION_") else None,
                        afd.nombre, pasos)
        return ResultadoLexico(original, normalizado, palabras, "DESCONOCIDO",
                               "sin_aceptacion",
                               "Sin contenido lexico" if not palabras else "Ningun AFD acepta")

    def clasificar(self, texto: str) -> str:
        return self.clasificar_detallado(texto).token

    def traza(self, texto: str) -> str:
        r = self.clasificar_detallado(texto)
        if r.automata is None:
            return f"{r.regla} -> DESCONOCIDO (usa --todos para ver cada recorrido)"
        lineas = [f"{r.automata}: {r.coincidencia!r}; inicio q0"]
        lineas += [f"q{a} -- {s!r} --> q{b}" for a, s, b in r.recorrido]
        return "\n".join(lineas + [f"Aceptacion: {r.estado_final} -> {r.token}"])


class AFDFrase:
    """AFD que reconoce una frase contigua en cualquier parte de la entrada.

    Sigma = palabras distintas de la frase + OTRO. No hay epsilon ni elecciones.
    delta se construye UNA vez; ejecutar solo consulta la tabla.
    Un sufijo que tambien sea prefijo permite reiniciar sin perder solapamientos.
    """
    OTRO = "<OTRO>"

    def __init__(self, token, frase):
        self.token, self.frase = token, frase
        self.patron = tuple(frase.split())
        self.final = len(self.patron)
        self.alfabeto = tuple(sorted(set(self.patron))) + (self.OTRO,)
        self.delta = {}
        for estado in range(self.final + 1):
            for simbolo in self.alfabeto:
                destino = self.final if estado == self.final else 0
                if estado != self.final:
                    candidato = self.patron[:estado] + (simbolo,)
                    for k in range(min(self.final, len(candidato)), 0, -1):
                        if candidato[-k:] == self.patron[:k]:
                            destino = k
                            break
                self.delta[estado, simbolo] = destino

    def ejecutar(self, simbolos):
        estado, pasos = 0, []
        for simbolo in simbolos:
            clase = simbolo if simbolo in self.alfabeto else self.OTRO
            destino = self.delta[estado, clase]
            pasos.append((estado, simbolo, destino))
            estado = destino
        return estado, tuple(pasos)
