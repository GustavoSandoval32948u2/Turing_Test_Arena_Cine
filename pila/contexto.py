# ============================================
# PILA DE CONTEXTO
# Responsable: Gencer Uriel (implementación)
# Integración: Gustavo Sandoval
# ============================================

class PilaContexto:
    def __init__(self):
        self.elementos = []  # La pila real

    def push(self, tema):
        """Guarda un nuevo tema en la pila"""
        self.elementos.append(tema)
        print(f"[PILA] Push → se guardó: '{tema}'")

    def pop(self):
        """Saca el último tema de la pila"""
        if self.esta_vacia():
            print("[PILA] Pop → la pila está vacía")
            return None
        tema = self.elementos.pop()
        print(f"[PILA] Pop → se sacó: '{tema}'")
        return tema

    def peek(self):
        """Mira el último tema sin sacarlo"""
        if self.esta_vacia():
            return None
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def mostrar(self):
        """Muestra el contenido actual de la pila (para depuración)"""
        if self.esta_vacia():
            print("[PILA] (vacía)")
        else:
            print(f"[PILA] Contenido actual: {self.elementos}")