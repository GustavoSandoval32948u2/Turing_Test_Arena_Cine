
from pila.contexto import PilaContexto
from plantillas.banco import BancoPlantillas


def ejecutar_pruebas():
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

    print("\n=== PRUEBAS DE LA PILA DE CONTEXTO ===")

    pila = PilaContexto()

    comprobar("la pila inicia vacía", pila.esta_vacia())
    comprobar("peek de pila vacía devuelve None", pila.peek() is None)

    pila.push("Titanic")
    comprobar("push guarda el tema", pila.peek() == "Titanic")

    pila.push("Tom Hanks")
    comprobar("la pila conserva el último tema", pila.peek() == "Tom Hanks")

    comprobar("pop devuelve el último tema", pila.pop() == "Tom Hanks")
    comprobar("pop restaura el tema anterior", pila.peek() == "Titanic")

    comprobar("pop devuelve el último elemento restante",
              pila.pop() == "Titanic")
    comprobar("la pila vuelve a quedar vacía", pila.esta_vacia())
    comprobar("pop de pila vacía devuelve None", pila.pop() is None)

    print("\n=== PRUEBAS DE PILA + PLANTILLAS ===")

    banco = BancoPlantillas(semilla=42)
    pila.push("Titanic")

    respuesta = banco.obtener(
        "HABLANDO_PELICULA",
        pila=pila,
        token="MENCION_PELICULA"
    )

    comprobar("la plantilla utiliza el tema de la pila",
              "Titanic" in respuesta)

    pila.pop()
    pila.push("Tom Hanks")

    respuesta = banco.obtener(
        "HABLANDO_ACTOR",
        pila=pila,
        token="MENCION_ACTOR"
    )

    comprobar("la plantilla utiliza el actor de la pila",
              "Tom Hanks" in respuesta)

    respuesta = banco.obtener(
        "CONVERSANDO",
        pila=pila,
        token="DESCONOCIDO"
    )

    comprobar("el banco responde en estado conversando",
              isinstance(respuesta, str) and bool(respuesta.strip()))

    errores = banco.validar_plantillas()
    comprobar("todas las plantillas siguen siendo válidas", not errores)

    print("\n" + "=" * 45)
    print(f"Resultado: {aprobadas}/{total} pruebas aprobadas.")

    if aprobadas != total:
        raise AssertionError("Hay pruebas fallidas.")

    print("Todos los componentes probados funcionan correctamente.")


if __name__ == "__main__":
    ejecutar_pruebas()
