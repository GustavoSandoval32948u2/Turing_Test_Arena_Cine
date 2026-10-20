# =========================================================
# TURING TEST ARENA - CINE
# PC DEL JUGADOR + TELEFONO DEL HUMANO
# CON TIEMPOS DE RESPUESTA SIMULADOS
# =========================================================

import json
import queue
import random
import socket
import threading
import time
import tkinter as tk

from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from tkinter import messagebox
from urllib.parse import parse_qs

from chatbot import ChatbotCine


# =========================================================
# CONFIGURACION
# =========================================================

PUERTO = 5050

# Tiempo de respuesta aparente
TIEMPO_MIN = 0000   # 3 segundos
TIEMPO_MAX = 0000   # 7 segundos

FONDO = "#10111F"
PANEL = "#191B2E"
PANEL_CLARO = "#22253D"
MORADO = "#8B5CF6"
CIAN = "#42E8E0"
ROSA = "#FF5C9A"
BLANCO = "#F5F5FF"
GRIS = "#A5A8C5"
VERDE = "#58E6A9"


# =========================================================
# DATOS COMPARTIDOS CON EL TELEFONO
# =========================================================

estado_web = {
    "mensaje": "",
    "participante": "",
    "hay_mensaje": False
}

cola_respuestas = queue.Queue()
lock_web = threading.Lock()


# =========================================================
# PAGINA DEL TELEFONO
# =========================================================

PAGINA_HTML = """
<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Participante Humano</title>

<style>

body {
    margin: 0;
    background: #10111F;
    color: #F5F5FF;
    font-family: Arial, sans-serif;
}

.contenedor {
    max-width: 600px;
    margin: auto;
    padding: 25px;
}

h1 {
    color: #42E8E0;
    font-size: 25px;
}

.estado {
    color: #58E6A9;
    margin-bottom: 25px;
}

.tarjeta {
    background: #191B2E;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}

#participante {
    color: #FF5C9A;
    font-weight: bold;
    margin-bottom: 12px;
}

#mensaje {
    font-size: 18px;
    line-height: 1.5;
}

textarea {
    width: 100%;
    box-sizing: border-box;
    background: #22253D;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 15px;
    font-size: 17px;
    min-height: 130px;
}

button {
    width: 100%;
    border: none;
    margin-top: 15px;
    padding: 15px;
    border-radius: 10px;
    background: #8B5CF6;
    color: white;
    font-size: 16px;
    font-weight: bold;
}

button:disabled {
    opacity: 0.5;
}

</style>

</head>

<body>

<div class="contenedor">

<h1>👤 PARTICIPANTE HUMANO</h1>

<div class="estado">
● CONECTADO AL JUEGO
</div>

<div class="tarjeta">

<div id="participante">
Esperando mensaje...
</div>

<div id="mensaje">
El jugador todavía no ha enviado nada.
</div>

</div>

<textarea
    id="respuesta"
    placeholder="Escribe aquí tu respuesta..."
    disabled>
</textarea>

<button
    id="boton"
    onclick="enviarRespuesta()"
    disabled>
ENVIAR RESPUESTA
</button>

</div>

<script>

async function actualizar() {

    try {

        const respuesta =
            await fetch("/estado");

        const datos =
            await respuesta.json();

        const participante =
            document.getElementById(
                "participante"
            );

        const mensaje =
            document.getElementById(
                "mensaje"
            );

        const entrada =
            document.getElementById(
                "respuesta"
            );

        const boton =
            document.getElementById(
                "boton"
            );

        if (datos.hay_mensaje) {

            participante.innerText =
                "Responde como PARTICIPANTE "
                + datos.participante;

            mensaje.innerText =
                datos.mensaje;

            entrada.disabled = false;
            boton.disabled = false;

        } else {

            participante.innerText =
                "Esperando mensaje...";

            mensaje.innerText =
                "El jugador todavía no ha enviado nada.";

            entrada.disabled = true;
            boton.disabled = true;
        }

    } catch (error) {

        console.log(error);

    }
}


async function enviarRespuesta() {

    const entrada =
        document.getElementById(
            "respuesta"
        );

    const texto =
        entrada.value.trim();

    if (!texto) {

        alert(
            "Escribe una respuesta."
        );

        return;
    }

    const datos =
        new URLSearchParams();

    datos.append(
        "respuesta",
        texto
    );

    await fetch(
        "/responder",
        {
            method: "POST",

            headers: {
                "Content-Type":
                "application/x-www-form-urlencoded"
            },

            body:
                datos.toString()
        }
    );

    entrada.value = "";

    actualizar();
}


setInterval(
    actualizar,
    800
);

actualizar();

</script>

</body>

</html>
"""


# =========================================================
# SERVIDOR WEB
# =========================================================

class ServidorHumano(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            contenido = PAGINA_HTML.encode(
                "utf-8"
            )

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                len(contenido)
            )

            self.end_headers()

            self.wfile.write(
                contenido
            )

        elif self.path == "/estado":

            with lock_web:

                datos = dict(
                    estado_web
                )

            contenido = json.dumps(
                datos,
                ensure_ascii=False
            ).encode(
                "utf-8"
            )

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )

            self.end_headers()

            self.wfile.write(
                contenido
            )

        else:

            self.send_error(404)

    def do_POST(self):

        if self.path != "/responder":

            self.send_error(404)
            return

        longitud = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )

        cuerpo = self.rfile.read(
            longitud
        ).decode(
            "utf-8"
        )

        datos = parse_qs(
            cuerpo
        )

        respuesta = datos.get(
            "respuesta",
            [""]
        )[0].strip()

        if respuesta:

            with lock_web:

                participante = (
                    estado_web[
                        "participante"
                    ]
                )

                estado_web[
                    "hay_mensaje"
                ] = False

                estado_web[
                    "mensaje"
                ] = ""

            cola_respuestas.put(
                (
                    participante,
                    respuesta
                )
            )

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            b"OK"
        )

    def log_message(
        self,
        format,
        *args
    ):
        return


# =========================================================
# INTERFAZ PRINCIPAL
# =========================================================

class InterfazCine:

    def __init__(
        self,
        root
    ):

        self.root = root

        self.root.title(
            "Turing Test Arena | Cine"
        )

        self.root.geometry(
            "1100x750"
        )

        self.root.minsize(
            820,
            600
        )

        self.root.configure(
            bg=FONDO
        )

        self.bot = ChatbotCine()

        # ---------------------------------------------
        # IDENTIDADES
        # ---------------------------------------------

        self.maquina = random.choice(
            ["A", "B"]
        )

        self.humano = (
            "B"
            if self.maquina == "A"
            else "A"
        )

        # ---------------------------------------------
        # ESTADO
        # ---------------------------------------------

        self.participante_actual = "A"

        self.mensajes = {
            "A": [],
            "B": []
        }

        self.partida_terminada = False

        self.esperando_respuesta = False

        self.participante_pendiente = None

        # Tiempo del mensaje enviado al humano
        self.inicio_espera_humano = None

        # Tiempo objetivo aleatorio del humano
        self.objetivo_humano = 0

        self.ip_local = (
            self._obtener_ip()
        )

        # ---------------------------------------------
        # CREAR
        # ---------------------------------------------

        self._crear_interfaz()

        self._mostrar_conversacion()

        self._iniciar_servidor()

        self.root.after(
            200,
            self._revisar_respuestas
        )

        self.entrada.focus_set()

    # =====================================================
    # IP
    # =====================================================

    def _obtener_ip(self):

        try:

            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
            )

            s.connect(
                (
                    "8.8.8.8",
                    80
                )
            )

            ip = (
                s.getsockname()[0]
            )

            s.close()

            return ip

        except Exception:

            return socket.gethostbyname(
                socket.gethostname()
            )

    # =====================================================
    # SERVIDOR
    # =====================================================

    def _iniciar_servidor(self):

        def ejecutar():

            try:

                servidor = (
                    ThreadingHTTPServer(
                        (
                            "0.0.0.0",
                            PUERTO
                        ),
                        ServidorHumano
                    )
                )

                print(
                    "[WEB] Servidor listo:"
                )

                print(
                    f"http://"
                    f"{self.ip_local}:"
                    f"{PUERTO}"
                )

                servidor.serve_forever()

            except Exception as error:

                print(
                    "[WEB] Error:",
                    error
                )

        hilo = threading.Thread(
            target=ejecutar,
            daemon=True
        )

        hilo.start()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def _crear_interfaz(self):

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header = tk.Frame(
            self.root,
            bg=PANEL,
            height=88
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        tk.Label(
            header,
            text=(
                "🎬 TURING TEST ARENA"
            ),
            font=(
                "Segoe UI",
                19,
                "bold"
            ),
            bg=PANEL,
            fg=BLANCO
        ).pack(
            side="left",
            padx=25,
            pady=22
        )

        tk.Label(
            header,
            text=(
                "CINE • HUMANO O MÁQUINA"
            ),
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=PANEL,
            fg=CIAN
        ).pack(
            side="right",
            padx=25
        )

        tk.Frame(
            self.root,
            bg=CIAN,
            height=2
        ).pack(
            fill="x"
        )

        # ---------------------------------------------
        # SUPERIOR
        # ---------------------------------------------

        superior = tk.Frame(
            self.root,
            bg=FONDO
        )

        superior.pack(
            fill="x",
            padx=25,
            pady=(15, 8)
        )

        tk.Label(
            superior,
            text=(
                "🍿 ¿Quién es humano "
                "y quién es máquina?"
            ),
            font=(
                "Segoe UI",
                16,
                "bold"
            ),
            bg=FONDO,
            fg=BLANCO
        ).pack(
            anchor="w"
        )

        tk.Label(
            superior,
            text=(
                "Habla con ambos participantes "
                "y descubre cuál es CineBot."
            ),
            font=(
                "Segoe UI",
                10
            ),
            bg=FONDO,
            fg=GRIS
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        tk.Label(
            superior,
            text=(
                "📱 Participante humano: "
                f"http://"
                f"{self.ip_local}:"
                f"{PUERTO}"
            ),
            font=(
                "Consolas",
                10,
                "bold"
            ),
            bg=FONDO,
            fg=VERDE
        ).pack(
            anchor="w",
            pady=(8, 0)
        )

        # ---------------------------------------------
        # SELECTOR
        # ---------------------------------------------

        selector = tk.Frame(
            self.root,
            bg=FONDO
        )

        selector.pack(
            fill="x",
            padx=25,
            pady=8
        )

        self.boton_a = tk.Button(
            selector,
            text="PARTICIPANTE A",
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            bg=MORADO,
            fg=BLANCO,
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=11,
            command=lambda:
                self.cambiar_participante(
                    "A"
                )
        )

        self.boton_a.pack(
            side="left",
            padx=(0, 10)
        )

        self.boton_b = tk.Button(
            selector,
            text="PARTICIPANTE B",
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            bg=PANEL_CLARO,
            fg=GRIS,
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=11,
            command=lambda:
                self.cambiar_participante(
                    "B"
                )
        )

        self.boton_b.pack(
            side="left"
        )

        self.estado = tk.Label(
            selector,
            text="● PARTIDA EN CURSO",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=FONDO,
            fg=VERDE
        )

        self.estado.pack(
            side="right"
        )

        # ---------------------------------------------
        # CHAT
        # ---------------------------------------------

        zona = tk.Frame(
            self.root,
            bg=FONDO
        )

        zona.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=5
        )

        self.canvas = tk.Canvas(
            zona,
            bg=FONDO,
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll = tk.Scrollbar(
            zona,
            command=self.canvas.yview
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=scroll.set
        )

        self.lista = tk.Frame(
            self.canvas,
            bg=FONDO
        )

        self.ventana_lista = (
            self.canvas.create_window(
                (0, 0),
                window=self.lista,
                anchor="nw"
            )
        )

        self.lista.bind(
            "<Configure>",
            self._actualizar_scroll
        )

        self.canvas.bind(
            "<Configure>",
            self._ajustar_ancho
        )

        # ---------------------------------------------
        # INFERIOR
        # ---------------------------------------------

        inferior = tk.Frame(
            self.root,
            bg=PANEL
        )

        inferior.pack(
            fill="x",
            side="bottom"
        )

        barra = tk.Frame(
            inferior,
            bg=PANEL
        )

        barra.pack(
            fill="x",
            padx=20,
            pady=(13, 7)
        )

        self.entrada = tk.Entry(
            barra,
            font=(
                "Segoe UI",
                12
            ),
            bg=PANEL_CLARO,
            fg=BLANCO,
            insertbackground=CIAN,
            relief="flat"
        )

        self.entrada.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 10)
        )

        self.entrada.bind(
            "<Return>",
            self._enviar_evento
        )

        self.boton_enviar = tk.Button(
            barra,
            text="ENVIAR ➤",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=MORADO,
            fg=BLANCO,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.enviar
        )

        self.boton_enviar.pack(
            side="right"
        )

        acciones = tk.Frame(
            inferior,
            bg=PANEL
        )

        acciones.pack(
            fill="x",
            padx=22,
            pady=(0, 12)
        )

        tk.Button(
            acciones,
            text="↻ Nueva partida",
            bg=PANEL,
            fg=CIAN,
            relief="flat",
            cursor="hand2",
            command=self.reiniciar
        ).pack(
            side="left"
        )

        # INDICADOR DE ESCRITURA
        self.escribiendo_label = tk.Label(
            acciones,
            text="",
            font=(
                "Segoe UI",
                9,
                "italic"
            ),
            bg=PANEL,
            fg=GRIS
        )

        self.escribiendo_label.pack(
            side="left",
            padx=25
        )

        tk.Button(
            acciones,
            text="🎯 IDENTIFICAR MÁQUINA",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=ROSA,
            fg=BLANCO,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.votar
        ).pack(
            side="right"
        )

    # =====================================================
    # CAMBIAR PARTICIPANTE
    # =====================================================

    def cambiar_participante(
        self,
        participante
    ):

        if self.esperando_respuesta:
            return

        self.participante_actual = (
            participante
        )

        self.boton_a.configure(
            bg=(
                MORADO
                if participante == "A"
                else PANEL_CLARO
            )
        )

        self.boton_b.configure(
            bg=(
                MORADO
                if participante == "B"
                else PANEL_CLARO
            )
        )

        self._mostrar_conversacion()

        self.entrada.focus_set()

    # =====================================================
    # MENSAJES
    # =====================================================

    def _mostrar_conversacion(self):

        for widget in (
            self.lista.winfo_children()
        ):
            widget.destroy()

        participante = (
            self.participante_actual
        )

        if not self.mensajes[
            participante
        ]:

            self._crear_burbuja(
                "SISTEMA",
                (
                    f"Conversación con "
                    f"Participante "
                    f"{participante}."
                ),
                "sistema"
            )

        for (
            remitente,
            texto,
            tipo,
            hora
        ) in self.mensajes[
            participante
        ]:

            self._crear_burbuja(
                remitente,
                texto,
                tipo,
                hora
            )

    def _guardar(
        self,
        participante,
        remitente,
        texto,
        tipo
    ):

        hora = (
            datetime.now().strftime(
                "%H:%M"
            )
        )

        self.mensajes[
            participante
        ].append(
            (
                remitente,
                texto,
                tipo,
                hora
            )
        )

        if (
            participante
            == self.participante_actual
        ):

            self._crear_burbuja(
                remitente,
                texto,
                tipo,
                hora
            )

    def _crear_burbuja(
        self,
        remitente,
        texto,
        tipo,
        hora=None
    ):

        fila = tk.Frame(
            self.lista,
            bg=FONDO
        )

        fila.pack(
            fill="x",
            padx=8,
            pady=7
        )

        usuario = (
            tipo == "usuario"
        )

        contenedor = tk.Frame(
            fila,
            bg=FONDO
        )

        contenedor.pack(
            anchor=(
                "e"
                if usuario
                else "w"
            )
        )

        color = (
            "#30244C"
            if usuario
            else PANEL
        )

        if tipo == "sistema":
            color = PANEL_CLARO

        tk.Label(
            contenedor,
            text=(
                remitente
                + (
                    f"  {hora}"
                    if hora
                    else ""
                )
            ),
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=FONDO,
            fg=(
                ROSA
                if usuario
                else CIAN
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            contenedor,
            text=texto,
            font=(
                "Segoe UI",
                10
            ),
            bg=color,
            fg=BLANCO,
            padx=15,
            pady=11,
            wraplength=520,
            justify="left"
        ).pack(
            pady=(4, 0)
        )

        self.root.after_idle(
            self._bajar
        )

    # =====================================================
    # ESTADO ESCRIBIENDO
    # =====================================================

    def _mostrar_escribiendo(
        self,
        participante
    ):

        self.escribiendo_label.configure(
            text=(
                f"Participante "
                f"{participante} "
                "está escribiendo..."
            )
        )

    def _ocultar_escribiendo(self):

        self.escribiendo_label.configure(
            text=""
        )

    def _bloquear_entrada(self):

        self.entrada.configure(
            state="disabled"
        )

        self.boton_enviar.configure(
            state="disabled"
        )

        self.boton_a.configure(
            state="disabled"
        )

        self.boton_b.configure(
            state="disabled"
        )

    def _desbloquear_entrada(self):

        if self.partida_terminada:
            return

        self.entrada.configure(
            state="normal"
        )

        self.boton_enviar.configure(
            state="normal"
        )

        self.boton_a.configure(
            state="normal"
        )

        self.boton_b.configure(
            state="normal"
        )

        self.entrada.focus_set()

    # =====================================================
    # ENVIAR
    # =====================================================

    def _enviar_evento(
        self,
        event
    ):

        self.enviar()

        return "break"

    def enviar(self):

        if (
            self.partida_terminada
            or self.esperando_respuesta
        ):
            return

        texto = (
            self.entrada.get().strip()
        )

        if not texto:
            return

        participante = (
            self.participante_actual
        )

        self.entrada.delete(
            0,
            "end"
        )

        self._guardar(
            participante,
            "TÚ",
            texto,
            "usuario"
        )

        self.esperando_respuesta = True

        self.participante_pendiente = (
            participante
        )

        self._bloquear_entrada()

        self._mostrar_escribiendo(
            participante
        )

        # =================================================
        # MAQUINA
        # =================================================

        if participante == self.maquina:

            try:

                respuesta = (
                    self.bot.procesar_entrada(
                        texto
                    )
                )

                if not respuesta:

                    respuesta = (
                        "Interesante. "
                        "Cuéntame un poco más."
                    )

            except Exception as error:

                print(
                    "[BOT]",
                    error
                )

                respuesta = (
                    "No estoy seguro de "
                    "cómo responder."
                )

            retraso = random.randint(
                TIEMPO_MIN,
                TIEMPO_MAX
            )

            self.root.after(
                retraso,
                lambda:
                    self._entregar_respuesta(
                        participante,
                        respuesta
                    )
            )

        # =================================================
        # HUMANO
        # =================================================

        else:

            self.inicio_espera_humano = (
                time.monotonic()
            )

            # Tiempo aparente objetivo
            # también entre 3 y 7 segundos
            self.objetivo_humano = (
                random.randint(
                    TIEMPO_MIN,
                    TIEMPO_MAX
                )
            )

            with lock_web:

                estado_web[
                    "mensaje"
                ] = texto

                estado_web[
                    "participante"
                ] = participante

                estado_web[
                    "hay_mensaje"
                ] = True

    # =====================================================
    # RECIBIR HUMANO
    # =====================================================

    def _revisar_respuestas(self):

        try:

            while True:

                participante, texto = (
                    cola_respuestas.get_nowait()
                )

                # Tiempo transcurrido desde
                # que se mandó la pregunta
                transcurrido = int(
                    (
                        time.monotonic()
                        - self.inicio_espera_humano
                    )
                    * 1000
                )

                restante = max(
                    0,
                    self.objetivo_humano
                    - transcurrido
                )

                # Si el humano respondió demasiado rápido,
                # esperamos un poco.
                # Si tardó bastante, mostramos inmediatamente.

                self.root.after(
                    restante,
                    lambda p=participante,
                    t=texto:
                        self._entregar_respuesta(
                            p,
                            t
                        )
                )

        except queue.Empty:
            pass

        self.root.after(
            200,
            self._revisar_respuestas
        )

    # =====================================================
    # ENTREGAR RESPUESTA
    # =====================================================

    def _entregar_respuesta(
        self,
        participante,
        respuesta
    ):

        self._guardar(
            participante,
            f"PARTICIPANTE "
            f"{participante}",
            respuesta,
            "respuesta"
        )

        self.esperando_respuesta = False

        self.participante_pendiente = None

        self._ocultar_escribiendo()

        self._desbloquear_entrada()

    # =====================================================
    # VOTACION
    # =====================================================

    def votar(self):

        if self.esperando_respuesta:
            return

        if (
            not self.mensajes["A"]
            or not self.mensajes["B"]
        ):

            messagebox.showwarning(
                "Faltan conversaciones",
                "Habla primero con "
                "A y B."
            )

            return

        ventana = tk.Toplevel(
            self.root
        )

        ventana.title(
            "Votación"
        )

        ventana.geometry(
            "400x260"
        )

        ventana.configure(
            bg=PANEL
        )

        tk.Label(
            ventana,
            text=(
                "¿QUIÉN ES LA MÁQUINA?"
            ),
            font=(
                "Segoe UI",
                16,
                "bold"
            ),
            bg=PANEL,
            fg=CIAN
        ).pack(
            pady=25
        )

        def elegir(opcion):

            ventana.destroy()

            self.partida_terminada = True

            self._bloquear_entrada()

            self.estado.configure(
                text=(
                    "● PARTIDA FINALIZADA"
                ),
                fg=ROSA
            )

            acerto = (
                opcion == self.maquina
            )

            texto = (
                "¡ACERTASTE!"
                if acerto
                else
                "¡LA MÁQUINA TE ENGAÑÓ!"
            )

            messagebox.showinfo(
                "Resultado",
                (
                    f"{texto}\n\n"
                    f"🤖 Máquina: "
                    f"Participante "
                    f"{self.maquina}\n"
                    f"👤 Humano: "
                    f"Participante "
                    f"{self.humano}"
                )
            )

        for opcion in (
            "A",
            "B"
        ):

            tk.Button(
                ventana,
                text=(
                    f"PARTICIPANTE "
                    f"{opcion}"
                ),
                bg=MORADO,
                fg=BLANCO,
                font=(
                    "Segoe UI",
                    11,
                    "bold"
                ),
                relief="flat",
                pady=10,
                command=lambda x=opcion:
                    elegir(x)
            ).pack(
                fill="x",
                padx=50,
                pady=5
            )

    # =====================================================
    # REINICIAR
    # =====================================================

    def reiniciar(self):

        if self.esperando_respuesta:

            messagebox.showwarning(
                "Espera",
                "Hay una respuesta "
                "pendiente."
            )

            return

        confirmar = (
            messagebox.askyesno(
                "Nueva partida",
                "¿Quieres comenzar "
                "una nueva partida?"
            )
        )

        if not confirmar:
            return

        self.bot.reiniciar()

        self.maquina = random.choice(
            ["A", "B"]
        )

        self.humano = (
            "B"
            if self.maquina == "A"
            else "A"
        )

        self.mensajes = {
            "A": [],
            "B": []
        }

        self.partida_terminada = False

        self.esperando_respuesta = False

        self.participante_actual = "A"

        self.estado.configure(
            text="● PARTIDA EN CURSO",
            fg=VERDE
        )

        self._ocultar_escribiendo()

        with lock_web:

            estado_web[
                "hay_mensaje"
            ] = False

            estado_web[
                "mensaje"
            ] = ""

            estado_web[
                "participante"
            ] = ""

        self._desbloquear_entrada()

        self.cambiar_participante(
            "A"
        )

    # =====================================================
    # SCROLL
    # =====================================================

    def _actualizar_scroll(
        self,
        event=None
    ):

        area = self.canvas.bbox(
            "all"
        )

        if area:

            self.canvas.configure(
                scrollregion=area
            )

    def _ajustar_ancho(
        self,
        event
    ):

        self.canvas.itemconfigure(
            self.ventana_lista,
            width=event.width
        )

    def _bajar(self):

        self.lista.update_idletasks()

        area = self.canvas.bbox(
            "all"
        )

        if area:

            self.canvas.configure(
                scrollregion=area
            )

            self.canvas.yview_moveto(
                1
            )


# =========================================================
# EJECUCION
# =========================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    app = InterfazCine(
        ventana
    )

    ventana.mainloop()