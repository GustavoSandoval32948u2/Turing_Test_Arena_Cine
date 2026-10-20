"""Verifica transiciones, limites, reinicio, solapamiento y trazas reales."""
from itertools import product
from afd.clasificador import ClasificadorAFD


def ejecutar():
    c = ClasificadorAFD()
    secuencias = 0
    for afd in c.automatas:
        assert len(afd.delta) == (afd.final + 1) * len(afd.alfabeto)
        assert all(isinstance(v, int) and 0 <= v <= afd.final for v in afd.delta.values())
        assert all(afd.delta[afd.final, s] == afd.final for s in afd.alfabeto)
        # Oraculo independiente: ventanas contiguas de palabras, sin usar delta.
        muestras = [(), afd.patron, ('zzz',) + afd.patron + ('zzz',),
                    afd.patron[:-1], afd.patron[:1] + afd.patron,
                    afd.patron[:1] + ('zzz',) + afd.patron[1:]]
        for n in range(min(afd.final + 2, 5)):
            muestras.extend(product(afd.alfabeto, repeat=n))
        for entrada in muestras:
            esperado = any(tuple(entrada[i:i+afd.final]) == afd.patron
                           for i in range(len(entrada) - afd.final + 1))
            estado, pasos = afd.ejecutar(entrada)
            assert (estado == afd.final) == esperado, (afd.frase, entrada)
            anterior = 0
            for a, s, b in pasos:
                assert a == anterior
                clase = s if s in afd.alfabeto else afd.OTRO
                assert b == afd.delta[a, clase]
                anterior = b
            assert len(pasos) == len(entrada) and anterior == estado
            secuencias += 1
    for entrada, esperado in [
        ('hasta hasta luego', 'DESPEDIDA'), ('hasta zzz luego', 'DESCONOCIDO'),
        ('holanda', 'DESCONOCIDO'), ('hola123', 'DESCONOCIDO'),
        ('ers un bot', 'DESCONOCIDO'), ('eres un botanico', 'DESCONOCIDO'),
        ('eres un un bot', 'DESCONOCIDO'), ('hola?actor', 'SALUDO'),
        ('¿?', 'DESCONOCIDO'), ('   ', 'DESCONOCIDO'),
    ]:
        assert c.clasificar(entrada) == esperado, entrada
    r = c.clasificar_detallado('eres un bot')
    assert r.recorrido == ((0, 'eres', 1), (1, 'un', 2), (2, 'bot', 3))
    assert c.clasificar('hola') == 'SALUDO'  # Ningun estado se conserva entre turnos.
    print(f'PASS: {len(c.automatas)} AFD; {secuencias} secuencias; tablas totales, trazas y casos limite.')


if __name__ == '__main__':
    ejecutar()
