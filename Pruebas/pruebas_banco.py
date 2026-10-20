
from plantillas.banco import BancoPlantillas
from definiciones import ESTADOS


def ejecutar_pruebas():
    banco = BancoPlantillas()
    aprobadas = 0
    total = 0

    # 1. Verificar que todos los estados tengan respuestas.
    for estado in ESTADOS:
        total += 1
        if estado in banco.PLANTILLAS and banco.PLANTILLAS[estado]:
            print(f"PASS: {estado} tiene respuestas.")
            aprobadas += 1
        else:
            print(f"FAIL: {estado} no tiene respuestas.")

    # 2. Verificar que las plantillas se puedan seleccionar.
    casos = [
        ("SALUDANDO", "SALUDO"),
        ("CONVERSANDO", "DESCONOCIDO"),
        ("HABLANDO_PELICULA", "MENCION_PELICULA"),
        ("HABLANDO_ACTOR", "MENCION_ACTOR"),
        ("HABLANDO_GENERO", "MENCION_GENERO"),
        ("OPINANDO", "OPINION"),
        ("PREGUNTANDO", "PREGUNTA"),
        ("PROVOCADO", "PROVOCACION"),
        ("DESPEDIDA", "DESPEDIDA"),
        ("FINAL", "DESCONOCIDO"),
    ]

    for estado, token in casos:
        total += 1
        try:
            respuesta = banco.obtener(estado, token=token)
            if isinstance(respuesta, str) and respuesta.strip():
                print(f"PASS: {estado} genera una respuesta.")
                aprobadas += 1
            else:
                print(f"FAIL: {estado} genera una respuesta vacía.")
        except Exception as error:
            print(f"FAIL: {estado}: {error}")

    # 3. Verificar que las entidades se inserten.
    entidades = [
        ("HABLANDO_PELICULA", "titanic"),
        ("HABLANDO_ACTOR", "Tom Hanks"),
        ("HABLANDO_GENERO", "comedia"),
    ]

    for estado, entidad in entidades:
        total += 1
        try:
            respuesta = banco.obtener(
                estado,
                token={
                    "HABLANDO_PELICULA": "MENCION_PELICULA",
                    "HABLANDO_ACTOR": "MENCION_ACTOR",
                    "HABLANDO_GENERO": "MENCION_GENERO",
                }[estado],
                entidad=entidad,
            )
            if entidad in respuesta:
                print(f"PASS: se insertó '{entidad}'.")
                aprobadas += 1
            else:
                print(f"FAIL: no se insertó '{entidad}'.")
        except Exception as error:
            print(f"FAIL: entidad {entidad}: {error}")

    print("-" * 40)
    print(f"Resultado: {aprobadas}/{total} pruebas aprobadas.")

    assert aprobadas == total, "Hay pruebas fallidas."


if __name__ == "__main__":
    ejecutar_pruebas()
