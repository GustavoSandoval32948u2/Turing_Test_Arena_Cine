
import subprocess
import sys
from pathlib import Path


CARPETA_PROYECTO = Path(__file__).resolve().parent

PRUEBAS = [
    ("Clasificador léxico", "pruebas_lexico.py"),
    ("Autómatas deterministas", "pruebas_afd.py"),
    ("Banco de plantillas", "pruebas_banco.py"),
    ("Pruebas completas del banco", "pruebas_banco_completo.py"),
    ("Pila y plantillas", "pruebas_componentes.py"),
]


def ejecutar_pruebas():
    aprobadas = 0
    fallidas = 0

    print("=" * 55)
    print("TURING TEST ARENA - EJECUTOR DE PRUEBAS")
    print("=" * 55)

    for nombre, archivo in PRUEBAS:
        print(f"\nEjecutando: {nombre}")
        print("-" * 55)

        resultado = subprocess.run(
            [sys.executable, str(CARPETA_PROYECTO / archivo)],
            cwd=CARPETA_PROYECTO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if resultado.stdout:
            print(resultado.stdout, end="")

        if resultado.stderr:
            print(resultado.stderr, end="")

        if resultado.returncode == 0:
            print(f"\nRESULTADO: PASS - {nombre}")
            aprobadas += 1
        else:
            print(f"\nRESULTADO: FAIL - {nombre}")
            fallidas += 1

    print("\n" + "=" * 55)
    print("RESUMEN GENERAL")
    print("=" * 55)
    print(f"Pruebas ejecutadas: {len(PRUEBAS)}")
    print(f"Archivos aprobados: {aprobadas}")
    print(f"Archivos con errores: {fallidas}")

    if fallidas == 0:
        print("\nTodas las suites finalizaron correctamente.")
        return 0

    print("\nHay errores que deben revisarse.")
    return 1


if __name__ == "__main__":
    sys.exit(ejecutar_pruebas())
