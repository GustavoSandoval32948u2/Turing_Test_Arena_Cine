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
}

# ------------------------------------------------
# 4. OPERACIONES DE PILA RECOMENDADAS
#    (Gencer las implementará, tú defines cuándo se usan)
# ------------------------------------------------
# - Cuando llega token MENCION_PELICULA  → push(nombre_pelicula)
# - Cuando llega token MENCION_ACTOR     → push(nombre_actor)
# - Cuando llega token MENCION_GENERO    → push(genero)
# - Cuando llega token RETOMAR_TEMA      → peek() o pop()
# - Al cambiar completamente de tema     → pop() + push(nuevo)