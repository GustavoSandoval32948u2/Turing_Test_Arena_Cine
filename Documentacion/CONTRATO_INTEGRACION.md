
# Contrato de integración — Turing Test Arena: Cine

## 1. Objetivo

Definir cómo se conectarán el AFD léxico, el AFN de diálogo, la pila de contexto, el banco de plantillas y la interfaz gráfica.

La integración debe respetar la arquitectura del proyecto y evitar dependencias innecesarias entre componentes.

## 2. Flujo general

1. El usuario escribe un mensaje en la interfaz.
2. El AFD clasifica el mensaje y devuelve un token.
3. El AFN recibe el estado actual y el token.
4. El AFN selecciona una transición válida. Si existen varias alternativas, debe elegir entre ellas mediante un mecanismo aleatorio real.
5. Se ejecutan las acciones de contexto que correspondan.
6. El banco selecciona una plantilla y personaliza la respuesta.
7. La interfaz muestra la respuesta y se conserva el estado actualizado.

## 3. Componentes existentes

### AFD léxico

Archivo: `afd/clasificador.py`

Responsabilidad:
- Clasificar el mensaje del usuario.
- Devolver una categoría léxica válida.
- Manejar entradas que no coincidan con categorías conocidas.

Tokens reconocidos:
- SALUDO
- DESPEDIDA
- PREGUNTA
- AFIRMACION
- NEGACION
- OPINION
- MENCION_PELICULA
- MENCION_ACTOR
- MENCION_GENERO
- RETOMAR_TEMA
- PROVOCACION
- DESCONOCIDO

La integración debe confirmar el nombre exacto de la clase y su método público.

### AFN de diálogo

Archivo: `afn/dialogo.py`

Responsabilidad:
- Recibir el estado actual y el token.
- Consultar las transiciones permitidas.
- Elegir aleatoriamente entre alternativas válidas.
- Determinar el nuevo estado.
- Informar las acciones de contexto que deben ejecutarse.

La interfaz pública deberá acordarse antes de integrar el componente con `chatbot.py`.

### Pila de contexto

Archivo: `pila/contexto.py`

Clase: `PilaContexto`

Métodos disponibles:
- `push(tema)`: guardar un tema.
- `pop()`: retirar y devolver el tema superior.
- `peek()`: consultar el tema superior sin retirarlo.
- `esta_vacia()`: comprobar si está vacía.
- `mostrar()`: mostrar su contenido.

La pila debe conservar el orden LIFO: el último tema guardado es el primero que se recupera.

### Banco de plantillas

Archivo: `plantillas/banco.py`

Clase: `BancoPlantillas`

Método principal:

`obtener(estado, pila=None, token="DESCONOCIDO", entidad=None)`

Responsabilidad:
- Seleccionar una respuesta asociada al estado.
- Utilizar respuestas específicas cuando corresponda.
- Personalizar respuestas con el tema recibido o recuperado de la pila.
- Proporcionar una respuesta alternativa si el estado no tiene plantillas.

### Interfaz gráfica

Archivo: `interfaz.py`

Responsabilidad:
- Recibir mensajes.
- Enviar el texto al chatbot.
- Mostrar las respuestas.
- Permitir limpiar la conversación.

La interfaz no debe implementar por su cuenta las reglas del AFN.

## 4. Responsabilidad del chatbot integrador

Archivo: `chatbot.py`

La clase `ChatbotCine` coordinará los componentes.

El método `procesar_entrada(texto_usuario)` deberá:

1. Clasificar el texto.
2. Obtener el token.
3. Consultar el AFN.
4. Actualizar el estado.
5. Ejecutar las acciones de contexto definidas.
6. Solicitar una respuesta al banco de plantillas.
7. Devolver una cadena de texto a la interfaz.

El chatbot integrador no debe duplicar las reglas de transición del AFN ni las plantillas.

## 5. Reglas de integración

- Los nombres de estados y tokens deben coincidir con `definiciones.py`.
- El AFN debe tener no determinismo real cuando existan varias transiciones válidas.
- Las decisiones del AFN deben distinguirse de las acciones sobre la pila.
- No se deben guardar temas duplicados sin una regla definida.
- Retomar un tema debe consultar el contexto y aplicar la operación de pila que corresponda.
- Ningún componente debe depender de la interfaz gráfica para funcionar.
- Los errores de integración deben poder identificarse mediante pruebas.

## 6. Pruebas existentes

- AFD léxico: 36/36 pruebas aprobadas.
- AFD completo: 157 autómatas y 7654 secuencias verificadas.
- Banco de plantillas: 74/74 pruebas aprobadas.
- Pila y plantillas: 13/13 pruebas aprobadas.

Estas pruebas validan componentes individuales y su integración parcial. Todavía no demuestran que el chatbot completo funcione.

## 7. Pendientes

- Terminar `afn/dialogo.py`.
- Confirmar la interfaz pública del AFN.
- Conectar los componentes en `chatbot.py`.
- Verificar las acciones de contexto durante una conversación.
- Ejecutar pruebas de conversaciones completas.
- Actualizar el diagrama para que coincida con el código definitivo.
- Documentar la justificación del no determinismo y el uso de la pila.

## 8. Criterio de aceptación

La integración se considerará funcional cuando un mensaje recorra todas las capas, produzca una respuesta coherente, actualice correctamente el estado y conserve el contexto cuando corresponda, con pruebas reproducibles.
