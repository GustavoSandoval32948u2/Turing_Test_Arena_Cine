"""Prueba manual de la capa lexica con las transiciones reales del AFD."""
import sys
from afd.clasificador import ClasificadorAFD


def main():
    clasificador = ClasificadorAFD()
    print("Prueba de AFD: escribe una frase o salir. --todos muestra cada AFD.")
    while True:
        try:
            entrada = input("\nEntrada: ")
        except (EOFError, KeyboardInterrupt):
            break
        if entrada.strip().lower() == "salir":
            break
        print(clasificador.traza(entrada))
        if "--todos" in sys.argv:
            for afd in clasificador.automatas:
                estado, pasos = afd.ejecutar(clasificador.simbolos(entrada))
                print(f"{afd.nombre} {afd.frase!r}: {pasos}; final q{estado}; acepta={estado == afd.final}")


if __name__ == "__main__":
    main()
