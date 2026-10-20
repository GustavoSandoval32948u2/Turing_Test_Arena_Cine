
from plantillas.banco import BancoPlantillas
from definiciones import ESTADOS


def ejecutar_pruebas():
    banco = BancoPlantillas(semilla=42)
    aprobadas = 0
    total = 0

    def comprobar(nombre, condicion):
        nonlocal aprobadas, total
        total += 1
        if condicion:
            aprobadas += 1
            print(f"PASS: {nombre}")
        else:
            print(f"FAIL: {nombre}")

    # 1. Todos los estados definidos deben tener plantillas.
    for estado in ESTADOS:
        comprobar(
            f"{estado} tiene plantillas",
            bool(banco.PLANTILLAS.get(estado))
        )

    # 2. Las plantillas deben ser válidas.
    errores = banco.validar_plantillas()
    comprobar("validación general de plantillas", not errores)

    # 3. Todos los temas deben aparecer en las respuestas.
    ejemplos = [
        ("HABLANDO_PELICULA", "MENCION_PELICULA", "Titanic"),
        ("HABLANDO_ACTOR", "MENCION_ACTOR", "Tom Hanks"),
        ("HABLANDO_GENERO", "MENCION_GENERO", "comedia"),
    ]

    for estado, token, tema in ejemplos:
        for intento in range(20):
            respuesta = banco.obtener(
                estado,
                token=token,
                entidad=tema
            )
            comprobar(
                f"{estado}: tema conservado ({intento + 1}/20)",
                tema in respuesta
            )

    # 4. Estado desconocido: debe producir una respuesta válida.
    respuesta = banco.obtener("ESTADO_INEXISTENTE")
    comprobar(
        "estado desconocido genera respuesta",
        isinstance(respuesta, str) and bool(respuesta.strip())
    )

    # 5. Entidad vacía: debe utilizar un tema alternativo.
    respuesta = banco.obtener(
        "HABLANDO_PELICULA",
        token="MENCION_PELICULA",
        entidad=""
    )
    comprobar(
        "entidad vacía no provoca error",
        isinstance(respuesta, str) and bool(respuesta.strip())
    )

    print("-" * 45)
    print(f"Resultado: {aprobadas}/{total} pruebas aprobadas.")

    if aprobadas != total:
        raise AssertionError("Hay pruebas fallidas en el banco.")


if __name__ == "__main__":
    ejecutar_pruebas()
