# ============================================
# DEFINICIONES OFICIALES - ARQUITECTURA
# Responsable: Gustavo Sandoval
# Tema: Cine
# ============================================

# ------------------------------------------------
# 1. TOKENS (salida del AFD - Capa Léxica)
# ------------------------------------------------
TOKENS = [
    "SALUDO",
    "DESPEDIDA",
    "PREGUNTA",
    "AFIRMACION",
    "NEGACION",
    "OPINION",
    "MENCION_PELICULA",
    "MENCION_ACTOR",
    "MENCION_GENERO",
    "RETOMAR_TEMA",
    "PROVOCACION",
    "DESCONOCIDO"
]

# ------------------------------------------------
# 2. ESTADOS DEL AFN (Capa de Diálogo)
# ------------------------------------------------
ESTADOS = [
    "INICIO",
    "SALUDANDO",
    "CONVERSANDO",
    "HABLANDO_PELICULA",
    "HABLANDO_ACTOR",
    "HABLANDO_GENERO",
    "OPINANDO",
    "PREGUNTANDO",
    "PROVOCADO",
    "DESPEDIDA",
    "FINAL"
]

ESTADO_INICIAL = "INICIO"

# ------------------------------------------------
# 3. TRANSICIONES PRINCIPALES (AFN)
#    Formato: (estado_actual, token) → [posibles estados siguientes]
#    El AFN elige uno al azar cuando hay más de una opción
#    (esto es el no-determinismo real)
# ------------------------------------------------
TRANSICIONES = {
    # Desde INICIO
    ("INICIO", "SALUDO"):          ["SALUDANDO"],
    ("INICIO", "DESCONOCIDO"):     ["CONVERSANDO"],
    ("INICIO", "PROVOCACION"): ["PROVOCADO"],
    
    # Desde SALUDANDO
    ("SALUDANDO", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("SALUDANDO", "MENCION_ACTOR"):    ["HABLANDO_ACTOR"],
    ("SALUDANDO", "MENCION_GENERO"):   ["HABLANDO_GENERO"],
    ("SALUDANDO", "PREGUNTA"):         ["PREGUNTANDO", "CONVERSANDO"],  # no-determinismo
    ("SALUDANDO", "DESPEDIDA"):        ["DESPEDIDA"],
    ("SALUDANDO", "DESCONOCIDO"):      ["CONVERSANDO"],
    
    # Desde CONVERSANDO
    ("CONVERSANDO", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("CONVERSANDO", "MENCION_ACTOR"):    ["HABLANDO_ACTOR"],
    ("CONVERSANDO", "MENCION_GENERO"):   ["HABLANDO_GENERO"],
    ("CONVERSANDO", "OPINION"):          ["OPINANDO", "CONVERSANDO"],  # no-determinismo
    ("CONVERSANDO", "PREGUNTA"):         ["PREGUNTANDO"],
    ("CONVERSANDO", "PROVOCACION"):      ["PROVOCADO"],
    ("CONVERSANDO", "DESPEDIDA"):        ["DESPEDIDA"],
    
    # Desde HABLANDO_PELICULA
    ("HABLANDO_PELICULA", "OPINION"):       ["OPINANDO"],
    ("HABLANDO_PELICULA", "PREGUNTA"):      ["PREGUNTANDO"],
    ("HABLANDO_PELICULA", "MENCION_ACTOR"): ["HABLANDO_ACTOR"],
    ("HABLANDO_PELICULA", "RETOMAR_TEMA"):  ["HABLANDO_PELICULA"],
    ("HABLANDO_PELICULA", "DESPEDIDA"):     ["DESPEDIDA"],
    ("HABLANDO_PELICULA", "DESCONOCIDO"):   ["CONVERSANDO", "HABLANDO_PELICULA"],  # no-determinismo
    
    # Desde HABLANDO_ACTOR
    ("HABLANDO_ACTOR", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("HABLANDO_ACTOR", "OPINION"):          ["OPINANDO"],
    ("HABLANDO_ACTOR", "DESPEDIDA"):        ["DESPEDIDA"],
    
    # Desde HABLANDO_GENERO
    ("HABLANDO_GENERO", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("HABLANDO_GENERO", "OPINION"):          ["OPINANDO"],
    ("HABLANDO_GENERO", "DESPEDIDA"):        ["DESPEDIDA"],
    
    # Desde OPINANDO
    ("OPINANDO", "AFIRMACION"):     ["CONVERSANDO"],
    ("OPINANDO", "NEGACION"):       ["CONVERSANDO"],
    ("OPINANDO", "PREGUNTA"):       ["PREGUNTANDO"],
    ("OPINANDO", "DESPEDIDA"):      ["DESPEDIDA"],
    
    # Desde PREGUNTANDO
    ("PREGUNTANDO", "AFIRMACION"):  ["CONVERSANDO"],
    ("PREGUNTANDO", "OPINION"):     ["OPINANDO"],
    ("PREGUNTANDO", "DESPEDIDA"):   ["DESPEDIDA"],
    
    # Desde PROVOCADO
    ("PROVOCADO", "DESPEDIDA"):     ["DESPEDIDA"],
    ("PROVOCADO", "DESCONOCIDO"):   ["CONVERSANDO", "PROVOCADO"],  # no-determinismo
    
    # Desde DESPEDIDA
    ("DESPEDIDA", "DESCONOCIDO"):   ["FINAL"],
    ("DESPEDIDA", "SALUDO"):        ["SALUDANDO"],  # por si saluda de nuevo

    # Continuidad de la conversacion
    ("SALUDANDO", "OPINION"): ["OPINANDO", "CONVERSANDO"],
    ("SALUDANDO", "AFIRMACION"): ["CONVERSANDO"],
    ("SALUDANDO", "NEGACION"): ["CONVERSANDO"],
    ("SALUDANDO", "PROVOCACION"): ["PROVOCADO"],

    ("CONVERSANDO", "AFIRMACION"): ["CONVERSANDO"],
    ("CONVERSANDO", "NEGACION"): ["CONVERSANDO"],
    ("CONVERSANDO", "RETOMAR_TEMA"): ["CONVERSANDO"],

    # Conversacion sobre peliculas
    ("HABLANDO_PELICULA", "MENCION_GENERO"): ["HABLANDO_GENERO"],
    ("HABLANDO_PELICULA", "PROVOCACION"): ["PROVOCADO"],
    ("HABLANDO_PELICULA", "AFIRMACION"): ["CONVERSANDO"],
    ("HABLANDO_PELICULA", "NEGACION"): ["CONVERSANDO"],

    # Conversacion sobre actores
    ("HABLANDO_ACTOR", "MENCION_GENERO"): ["HABLANDO_GENERO"],
    ("HABLANDO_ACTOR", "MENCION_ACTOR"): ["HABLANDO_ACTOR"],
    ("HABLANDO_ACTOR", "OPINION"): ["OPINANDO"],
    ("HABLANDO_ACTOR", "PREGUNTA"): ["PREGUNTANDO", "HABLANDO_ACTOR"],
    ("HABLANDO_ACTOR", "PROVOCACION"): ["PROVOCADO"],
    ("HABLANDO_ACTOR", "RETOMAR_TEMA"): ["HABLANDO_ACTOR"],
    ("HABLANDO_ACTOR", "DESCONOCIDO"): ["CONVERSANDO", "HABLANDO_ACTOR"],
    ("HABLANDO_ACTOR", "AFIRMACION"): ["CONVERSANDO"],
    ("HABLANDO_ACTOR", "NEGACION"): ["CONVERSANDO"],

    # Conversacion sobre generos
    ("HABLANDO_GENERO", "MENCION_ACTOR"): ["HABLANDO_ACTOR"],
    ("HABLANDO_GENERO", "MENCION_GENERO"): ["HABLANDO_GENERO"],
    ("HABLANDO_GENERO", "PREGUNTA"): ["PREGUNTANDO", "HABLANDO_GENERO"],
    ("HABLANDO_GENERO", "PROVOCACION"): ["PROVOCADO"],
    ("HABLANDO_GENERO", "RETOMAR_TEMA"): ["HABLANDO_GENERO"],
    ("HABLANDO_GENERO", "DESCONOCIDO"): ["CONVERSANDO", "HABLANDO_GENERO"],
    ("HABLANDO_GENERO", "AFIRMACION"): ["CONVERSANDO"],
    ("HABLANDO_GENERO", "NEGACION"): ["CONVERSANDO"],

    # Opinion y preguntas
    ("OPINANDO", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("OPINANDO", "MENCION_ACTOR"): ["HABLANDO_ACTOR"],
    ("OPINANDO", "MENCION_GENERO"): ["HABLANDO_GENERO"],
    ("OPINANDO", "PROVOCACION"): ["PROVOCADO"],
    ("OPINANDO", "DESCONOCIDO"): ["CONVERSANDO", "OPINANDO"],

    ("PREGUNTANDO", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("PREGUNTANDO", "MENCION_ACTOR"): ["HABLANDO_ACTOR"],
    ("PREGUNTANDO", "MENCION_GENERO"): ["HABLANDO_GENERO"],
    ("PREGUNTANDO", "PROVOCACION"): ["PROVOCADO"],
    ("PREGUNTANDO", "NEGACION"): ["CONVERSANDO"],
    ("PREGUNTANDO", "DESCONOCIDO"): ["CONVERSANDO", "PREGUNTANDO"],

    # Respuesta a provocaciones
    ("PROVOCADO", "SALUDO"): ["SALUDANDO"],
    ("PROVOCADO", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("PROVOCADO", "MENCION_ACTOR"): ["HABLANDO_ACTOR"],
    ("PROVOCADO", "MENCION_GENERO"): ["HABLANDO_GENERO"],
    ("PROVOCADO", "PREGUNTA"): ["PREGUNTANDO"],
    ("PROVOCADO", "OPINION"): ["OPINANDO"],
    ("PROVOCADO", "AFIRMACION"): ["CONVERSANDO"],
    ("PROVOCADO", "NEGACION"): ["CONVERSANDO"],

    # Reiniciar una conversacion despues de despedirse
    ("FINAL", "SALUDO"): ["SALUDANDO"],
    ("FINAL", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("FINAL", "MENCION_ACTOR"): ["HABLANDO_ACTOR"],
    ("FINAL", "MENCION_GENERO"): ["HABLANDO_GENERO"],
    ("FINAL", "DESPEDIDA"): ["FINAL"],
    ("FINAL", "DESCONOCIDO"): ["CONVERSANDO"],

        # Cambio de película sin salir del estado temático
    ("HABLANDO_PELICULA", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],

    # Preguntas consecutivas
    ("PREGUNTANDO", "PREGUNTA"): ["PREGUNTANDO"],

    # Nuevas preguntas después de opinar
    ("OPINANDO", "OPINION"): ["OPINANDO"],

    # Cambios de tema desde una conversación general
    ("INICIO", "MENCION_PELICULA"): ["HABLANDO_PELICULA"],
    ("INICIO", "MENCION_ACTOR"): ["HABLANDO_ACTOR"],
    ("INICIO", "MENCION_GENERO"): ["HABLANDO_GENERO"],
    ("INICIO", "PREGUNTA"): ["PREGUNTANDO"],
    ("INICIO", "DESPEDIDA"): ["DESPEDIDA"],

}

