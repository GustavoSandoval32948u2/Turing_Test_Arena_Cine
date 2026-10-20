# =========================================================
# TURING TEST ARENA - CINE
# PC DEL PARTICIPANTE HUMANO
# =========================================================

import json
import queue
import socket
import threading
import tkinter as tk
from tkinter import messagebox


PUERTO = 5050

FONDO = "#10111F"
PANEL = "#191B2E"
PANEL_CLARO = "#22253D"
MORADO = "#8B5CF6"
CIAN = "#42E8E0"
ROSA = "#FF5C9A"
BLANCO = "#F5F5FF"
GRIS = "#A5A8C5"
VERDE = "#58E6A9"
ROJO = "#FF6B6B"


class ParticipanteHumano:

    def __init__(self, root):

        self.root = root
        self.root.title(
            "Turing Test Arena | Participante Humano"
        )

        self.root.geometry(
            "720x570"
        )

        self.root.minsize(
            600,
            500
        )

        self.root.configure(
            bg=FONDO
        )

        self.socket = None
        self.conectado = False

        self.participante_actual = None
        self.mensaje_actual = None

        self.cola = queue.Queue()
        self.lock = threading.Lock()

        self._crear_interfaz()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar
        )

        self.root.after(
            100,
            self._procesar_cola
        )

    # =====================================================
    # INTERFAZ
    # =====================================================

    def _crear_interfaz(self):

        header = tk.Frame(
            self.root,
            bg=PANEL
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="👤 PARTICIPANTE HUMANO",
            font=("Segoe UI", 18, "bold"),
            bg=PANEL,
            fg=BLANCO
        ).pack(
            side="left",
            padx=22,
            pady=20
        )

        self.estado = tk.Label(
            header,
            text="● DESCONECTADO",
            font=("Segoe UI", 9, "bold"),
            bg=PANEL,
            fg=ROJO
        )

        self.estado.pack(
            side="right",
            padx=22
        )

        tk.Frame(
            self.root,
            bg=CIAN,
            height=2
        ).pack(fill="x")

        # -------------------------------------------------
        # CONEXION
        # -------------------------------------------------

        conexion = tk.Frame(
            self.root,
            bg=FONDO
        )

        conexion.pack(
            fill="x",
            padx=25,
            pady=20
        )

        tk.Label(
            conexion,
            text="IP DE LA COMPUTADORA DEL JUGADOR",
            font=("Segoe UI", 9, "bold"),
            bg=FONDO,
            fg=GRIS
        ).pack(
            anchor="w"
        )

        fila_ip = tk.Frame(
            conexion,
            bg=FONDO
        )

        fila_ip.pack(
            fill="x",
            pady=(7, 0)
        )

        self.entrada_ip = tk.Entry(
            fila_ip,
            font=("Consolas", 12),
            bg=PANEL_CLARO,
            fg=BLANCO,
            insertbackground=CIAN,
            relief="flat"
        )

        self.entrada_ip.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 10)
        )

        self.entrada_ip.insert(
            0,
            "192.168.1."
        )

        self.boton_conectar = tk.Button(
            fila_ip,
            text="CONECTAR",
            font=("Segoe UI", 10, "bold"),
            bg=MORADO,
            fg=BLANCO,
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=10,
            command=self.conectar
        )

        self.boton_conectar.pack(
            side="right"
        )

        # -------------------------------------------------
        # INFORMACION
        # -------------------------------------------------

        self.info_participante = tk.Label(
            self.root,
            text=(
                "Conéctate para comenzar."
            ),
            font=("Segoe UI", 13, "bold"),
            bg=FONDO,
            fg=CIAN
        )

        self.info_participante.pack(
            padx=25,
            pady=(5, 12),
            anchor="w"
        )

        tk.Label(
            self.root,
            text="MENSAJE DEL JUGADOR",
            font=("Segoe UI", 9, "bold"),
            bg=FONDO,
            fg=GRIS
        ).pack(
            padx=25,
            anchor="w"
        )

        self.mensaje_label = tk.Label(
            self.root,
            text=(
                "Esperando un mensaje..."
            ),
            font=("Segoe UI", 12),
            bg=PANEL_CLARO,
            fg=BLANCO,
            wraplength=640,
            justify="left",
            anchor="w",
            padx=18,
            pady=18
        )

        self.mensaje_label.pack(
            fill="x",
            padx=25,
            pady=(8, 18)
        )

        tk.Label(
            self.root,
            text="TU RESPUESTA",
            font=("Segoe UI", 9, "bold"),
            bg=FONDO,
            fg=GRIS
        ).pack(
            padx=25,
            anchor="w"
        )

        self.respuesta = tk.Text(
            self.root,
            height=7,
            font=("Segoe UI", 11),
            bg=PANEL_CLARO,
            fg=BLANCO,
            insertbackground=CIAN,
            relief="flat",
            wrap="word"
        )

        self.respuesta.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(8, 13)
        )

        self.boton_enviar = tk.Button(
            self.root,
            text="ENVIAR RESPUESTA ➤",
            font=("Segoe UI", 11, "bold"),
            bg=MORADO,
            fg=BLANCO,
            activebackground="#7543D8",
            activeforeground=BLANCO,
            relief="flat",
            cursor="hand2",
            pady=12,
            command=self.enviar_respuesta
        )

        self.boton_enviar.pack(
            fill="x",
            padx=25,
            pady=(0, 22)
        )

        self.respuesta.configure(
            state="disabled"
        )

        self.boton_enviar.configure(
            state="disabled"
        )

    # =====================================================
    # CONEXION
    # =====================================================

    def conectar(self):

        if self.conectado:
            return

        ip = self.entrada_ip.get().strip()

        if not ip:

            messagebox.showwarning(
                "IP",
                "Escribe la IP de la "
                "computadora principal."
            )

            return

        self.boton_conectar.configure(
            state="disabled"
        )

        self.estado.configure(
            text="● CONECTANDO...",
            fg=CIAN
        )

        hilo = threading.Thread(
            target=self._conectar_hilo,
            args=(ip,),
            daemon=True
        )

        hilo.start()

    def _conectar_hilo(
        self,
        ip
    ):

        try:

            cliente = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            cliente.connect(
                (
                    ip,
                    PUERTO
                )
            )

            with self.lock:
                self.socket = cliente

            self.conectado = True

            self.cola.put(
                ("conectado", None)
            )

            self._escuchar_servidor(
                cliente
            )

        except Exception as error:

            self.cola.put(
                (
                    "error",
                    str(error)
                )
            )

        finally:

            self.conectado = False

            with self.lock:

                if self.socket:

                    try:
                        self.socket.close()
                    except Exception:
                        pass

                    self.socket = None

            self.cola.put(
                ("desconectado", None)
            )

    # =====================================================
    # RECIBIR
    # =====================================================

    def _escuchar_servidor(
        self,
        cliente
    ):

        buffer = ""

        while self.conectado:

            datos = cliente.recv(
                4096
            )

            if not datos:
                break

            buffer += datos.decode(
                "utf-8"
            )

            while "\n" in buffer:

                linea, buffer = (
                    buffer.split(
                        "\n",
                        1
                    )
                )

                linea = linea.strip()

                if not linea:
                    continue

                try:

                    mensaje = (
                        json.loads(linea)
                    )

                    if (
                        mensaje.get("tipo")
                        == "pregunta"
                    ):

                        self.cola.put(
                            (
                                "pregunta",
                                mensaje
                            )
                        )

                except json.JSONDecodeError:
                    pass

    # =====================================================
    # PROCESAR EVENTOS
    # =====================================================

    def _procesar_cola(self):

        try:

            while True:

                tipo, datos = (
                    self.cola.get_nowait()
                )

                if tipo == "conectado":

                    self.estado.configure(
                        text="● CONECTADO",
                        fg=VERDE
                    )

                    self.boton_conectar.configure(
                        text="CONECTADO",
                        state="disabled"
                    )

                    self.entrada_ip.configure(
                        state="disabled"
                    )

                    self.info_participante.configure(
                        text=(
                            "Conexión lista. "
                            "Esperando al jugador..."
                        )
                    )

                elif tipo == "pregunta":

                    self.participante_actual = (
                        datos.get(
                            "participante"
                        )
                    )

                    self.mensaje_actual = (
                        datos.get(
                            "texto",
                            ""
                        )
                    )

                    self.info_participante.configure(
                        text=(
                            "Responde como "
                            f"PARTICIPANTE "
                            f"{self.participante_actual}"
                        )
                    )

                    self.mensaje_label.configure(
                        text=self.mensaje_actual
                    )

                    self.respuesta.configure(
                        state="normal"
                    )

                    self.respuesta.delete(
                        "1.0",
                        "end"
                    )

                    self.boton_enviar.configure(
                        state="normal"
                    )

                    self.respuesta.focus_set()

                elif tipo == "error":

                    messagebox.showerror(
                        "Conexión",
                        (
                            "No fue posible conectarse.\n\n"
                            f"{datos}"
                        )
                    )

                elif tipo == "desconectado":

                    self.estado.configure(
                        text="● DESCONECTADO",
                        fg=ROJO
                    )

                    self.boton_conectar.configure(
                        text="CONECTAR",
                        state="normal"
                    )

                    self.entrada_ip.configure(
                        state="normal"
                    )

                    self.info_participante.configure(
                        text=(
                            "Conéctate para comenzar."
                        )
                    )

                    self.respuesta.configure(
                        state="disabled"
                    )

                    self.boton_enviar.configure(
                        state="disabled"
                    )

        except queue.Empty:
            pass

        if self.root.winfo_exists():

            self.root.after(
                100,
                self._procesar_cola
            )

    # =====================================================
    # ENVIAR RESPUESTA
    # =====================================================

    def enviar_respuesta(self):

        if not self.conectado:
            return

        if not self.participante_actual:
            return

        texto = self.respuesta.get(
            "1.0",
            "end"
        ).strip()

        if not texto:

            messagebox.showwarning(
                "Respuesta",
                "Escribe una respuesta."
            )

            return

        mensaje = {
            "tipo": "respuesta",
            "participante":
                self.participante_actual,
            "texto": texto
        }

        datos = (
            json.dumps(
                mensaje,
                ensure_ascii=False
            )
            + "\n"
        ).encode("utf-8")

        try:

            with self.lock:

                if not self.socket:
                    raise ConnectionError(
                        "No existe conexión."
                    )

                self.socket.sendall(
                    datos
                )

            self.respuesta.delete(
                "1.0",
                "end"
            )

            self.respuesta.configure(
                state="disabled"
            )

            self.boton_enviar.configure(
                state="disabled"
            )

            self.mensaje_label.configure(
                text=(
                    "Respuesta enviada.\n\n"
                    "Esperando otro mensaje..."
                )
            )

            self.info_participante.configure(
                text=(
                    "Respuesta enviada correctamente."
                )
            )

            self.participante_actual = None
            self.mensaje_actual = None

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "No se pudo enviar "
                    "la respuesta.\n\n"
                    f"{error}"
                )
            )

    # =====================================================
    # CERRAR
    # =====================================================

    def cerrar(self):

        self.conectado = False

        with self.lock:

            if self.socket:

                try:
                    self.socket.shutdown(
                        socket.SHUT_RDWR
                    )
                except Exception:
                    pass

                try:
                    self.socket.close()
                except Exception:
                    pass

                self.socket = None

        self.root.destroy()


# =========================================================
# EJECUCION
# =========================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    app = ParticipanteHumano(
        ventana
    )

    ventana.mainloop()