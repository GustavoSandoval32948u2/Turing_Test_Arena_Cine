
from chatbot import ChatbotCine

bot = ChatbotCine(semilla=42)

pruebas = [
    # Conversacion inicial
    "Hola",
    "Hablemos de Inception",
    "¿De qué trata?",
    "Me gustó mucho",
    "Sí",
    "No",

    # Cambio de pelicula
    "Hablemos de Titanic",
    "¿Quiénes son los actores?",

    # Actores
    "Hablemos de Leonardo DiCaprio",
    "¿Qué películas ha hecho?",

    # Generos
    "Hablemos de terror",
    "¿Qué opinas del terror?",

    # Provocaciones
    "¿Eres un bot?",
    "No pareces humano",

    # Recuperar temas
    "Volvamos al tema anterior",
    "Volvamos al tema anterior",

    # Preguntas generales
    "Recomiéndame una película",
    "¿Qué película es mejor?",

    # Desconocidos
    "Hablemos de una película inventada XYZ123",

    # Despedida
    "Adiós",
]

print("\n========== PRUEBAS FINALES ==========\n")

for numero, mensaje in enumerate(pruebas, start=1):
    print(f"\n{'=' * 55}")
    print(f"PRUEBA {numero}")
    print(f"TÚ: {mensaje}")

    try:
        respuesta = bot.procesar_entrada(mensaje)
        print(f"CINEBOT: {respuesta}")

    except Exception as error:
        print(f"ERROR EN PRUEBA {numero}: {error}")
        raise

print("\n========== PRUEBA DE REINICIO ==========\n")

bot.reiniciar()

print("Estado:", bot.obtener_estado())
print("Contexto:", bot.obtener_contexto())

assert bot.obtener_estado() == "INICIO"
assert bot.obtener_contexto()["tema"] is None
assert bot.obtener_contexto()["cantidad_temas"] == 0

print("\nREINICIO CORRECTO")
print("\n========== FIN DE PRUEBAS ==========")
