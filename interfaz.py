
import tkinter as tk
from tkinter import scrolledtext
from chatbot import ChatbotCine


class InterfazChatbot:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Turing Test Arena - Cine")
        self.ventana.geometry("700x550")
        self.ventana.minsize(500, 400)
        self.ventana.configure(bg="#20242c")

        self.bot = ChatbotCine()

        titulo = tk.Label(
            ventana,
            text="TURING TEST ARENA",
            font=("Arial", 20, "bold"),
            bg="#20242c",
            fg="#61dafb"
        )
        titulo.pack(pady=(15, 0))

        subtitulo = tk.Label(
            ventana,
            text="Chatbot de conversación sobre cine",
            font=("Arial", 11),
            bg="#20242c",
            fg="white"
        )
        subtitulo.pack(pady=(3, 12))

        self.conversacion = scrolledtext.ScrolledText(
            ventana,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg="#2b303b",
            fg="white",
            insertbackground="white",
            state=tk.DISABLED
        )
        self.conversacion.pack(
            fill=tk.BOTH,
            expand=True,
            padx=15,
            pady=5
        )

        self.conversacion.tag_config(
            "usuario", foreground="#61dafb"
        )
        self.conversacion.tag_config(
            "bot", foreground="#a8e6a3"
        )
        self.conversacion.tag_config(
            "sistema", foreground="#cccccc"
        )

        zona_entrada = tk.Frame(ventana, bg="#20242c")
        zona_entrada.pack(fill=tk.X, padx=15, pady=12)

        self.entrada = tk.Entry(
            zona_entrada,
            font=("Arial", 12),
            bg="#ffffff"
        )
        self.entrada.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            ipady=8
        )
        self.entrada.bind("<Return>", self.enviar_mensaje)

        boton_enviar = tk.Button(
            zona_entrada,
            text="Enviar",
            command=self.enviar_mensaje,
            bg="#1677c8",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15
        )
        boton_enviar.pack(side=tk.LEFT, padx=(8, 0))

        boton_limpiar = tk.Button(
            ventana,
            text="Limpiar conversación",
            command=self.limpiar_conversacion,
            bg="#444b57",
            fg="white"
        )
        boton_limpiar.pack(pady=(0, 12))

        self.mostrar_mensaje(
            "Sistema",
            "¡Bienvenido! Escribe un mensaje para comenzar.",
            "sistema"
        )
        self.entrada.focus_set()

    def mostrar_mensaje(self, emisor, mensaje, etiqueta):
        self.conversacion.config(state=tk.NORMAL)
        self.conversacion.insert(
            tk.END, f"{emisor}: ", etiqueta
        )
        self.conversacion.insert(tk.END, f"{mensaje}\n\n")
        self.conversacion.config(state=tk.DISABLED)
        self.conversacion.see(tk.END)

    def enviar_mensaje(self, evento=None):
        texto = self.entrada.get().strip()

        if not texto:
            return

        self.entrada.delete(0, tk.END)
        self.mostrar_mensaje("Tú", texto, "usuario")

        if texto.lower() in ("salir", "exit", "quit"):
            respuesta = "¡Hasta pronto! Gracias por conversar."
        else:
            try:
                respuesta = self.bot.procesar_entrada(texto)
            except Exception as error:
                respuesta = f"Ocurrió un error al procesar el mensaje: {error}"

        self.mostrar_mensaje("Bot", respuesta, "bot")

    def limpiar_conversacion(self):
        self.conversacion.config(state=tk.NORMAL)
        self.conversacion.delete("1.0", tk.END)
        self.conversacion.config(state=tk.DISABLED)
        self.mostrar_mensaje(
            "Sistema",
            "Conversación limpiada. Puedes comenzar de nuevo.",
            "sistema"
        )
        self.entrada.focus_set()


if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = InterfazChatbot(ventana)
    ventana.mainloop()
