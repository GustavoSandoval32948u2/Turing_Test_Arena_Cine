# ============================================
# QA DE CLASIFICACION - CAPA LEXICA / AFD
# Responsable: Edin Adolfo
# ============================================

from afd.clasificador import ClasificadorAFD
from definiciones import TOKENS


CASOS = [
    # Regresion de la frase reportada y limites de palabra.
    ("eres un bot", "PROVOCACION", "regresion"),
    ("¿ERES UN BOT?", "PROVOCACION", "regresion"),
    ("eres un bot de cine", "PROVOCACION", "regresion"),
    ("eres un botanico", "DESCONOCIDO", "limite"),
    # Casos normales: al menos uno por clasificador/token.
    ("Hola, buenas tardes", "SALUDO", "normal"),
    ("Hasta luego, nos vemos", "DESPEDIDA", "normal"),
    ("Que pelicula recomiendas?", "PREGUNTA", "normal"),
    ("Si, claro", "AFIRMACION", "normal"),
    ("No, para nada", "NEGACION", "normal"),
    ("Creo que es una excelente pelicula", "OPINION", "normal"),
    ("Hablemos de Titanic", "MENCION_PELICULA", "normal"),
    ("Me gusta Leonardo DiCaprio", "MENCION_ACTOR", "normal"),
    ("Prefiero ciencia ficcion", "MENCION_GENERO", "normal"),
    ("Volvamos al tema anterior", "RETOMAR_TEMA", "normal"),
    ("Eres un inutil", "PROVOCACION", "normal"),
    ("xyz 123 cosa", "DESCONOCIDO", "normal"),

    # Casos ambiguos: prueban la prioridad determinista.
    ("Hola, que opinas de Titanic?", "SALUDO", "ambiguo"),
    ("Que opinas de Titanic?", "MENCION_PELICULA", "ambiguo"),
    ("No me gusta Avatar", "MENCION_PELICULA", "ambiguo"),
    ("Es bueno Tom Hanks?", "MENCION_ACTOR", "ambiguo"),
    ("Te gusta el terror?", "MENCION_GENERO", "ambiguo"),
    ("Adios, tonto", "PROVOCACION", "ambiguo"),

    # Casos limite.
    ("", "DESCONOCIDO", "limite"),
    ("   !!!   ", "DESCONOCIDO", "limite"),
    ("HÓLÁ", "SALUDO", "limite"),
    ("¿QUÉ TAL?", "SALUDO", "limite"),
    ("TITANIC!!!", "MENCION_PELICULA", "limite"),
    ("accion", "MENCION_GENERO", "limite"),

    # Casos tomados directamente del diagrama AFD entregado por el grupo.
    ("hey", "SALUDO", "diagrama"),
    ("bye", "DESPEDIDA", "diagrama"),
    ("quiero una peli", "MENCION_PELICULA", "diagrama"),
    ("el protagonista fue excelente", "MENCION_ACTOR", "diagrama"),
    ("prefiero comedia", "MENCION_GENERO", "diagrama"),
    ("odio esa historia", "OPINION", "diagrama"),
    ("como funciona", "PREGUNTA", "diagrama"),
    ("no sabes nada", "PROVOCACION", "diagrama"),
]


def ejecutar_pruebas(verbose=True):
    afd = ClasificadorAFD()
    aprobadas = 0
    tokens_probados = set()

    print("=" * 72)
    print("QA AFD / CAPA LEXICA - EDIN ADOLFO")
    print("=" * 72)

    for i, (entrada, esperado, tipo) in enumerate(CASOS, 1):
        resultado = afd.clasificar_detallado(entrada)
        ok = resultado.token == esperado
        if ok:
            aprobadas += 1
        tokens_probados.add(resultado.token)

        if verbose:
            marca = "PASS" if ok else "FAIL"
            print(f"{i:02d}. {marca} [{tipo.upper()}]")
            print(f"    Entrada : {entrada!r}")
            print(f"    Esperado: {esperado}")
            print(f"    Obtenido: {resultado.token}")
            print(f"    Estado  : {resultado.estado_final}")
            print(f"    Regla   : {resultado.regla}")

    faltantes = set(TOKENS) - tokens_probados
    print("-" * 72)
    print(f"Resultado: {aprobadas}/{len(CASOS)} pruebas aprobadas")
    print("Cobertura de tokens:", ", ".join(sorted(tokens_probados)))
    if faltantes:
        print("Tokens sin cubrir:", ", ".join(sorted(faltantes)))
    else:
        print("PASS - Las pruebas cubren TODOS los clasificadores definidos.")

    assert aprobadas == len(CASOS), "Hay pruebas de clasificacion que fallaron."
    assert not faltantes, "No se cubrieron todos los tokens del proyecto."
    return True


if __name__ == "__main__":
    ejecutar_pruebas()
