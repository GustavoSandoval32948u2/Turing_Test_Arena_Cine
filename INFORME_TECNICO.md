
# Informe técnico de implementación y pruebas
## Proyecto: Turing Test Arena — Cine

### 1. Introducción

Turing Test Arena — Cine es un chatbot diseñado para mantener conversaciones sobre películas, actores y géneros cinematográficos mediante autómatas y estructuras de datos. El proyecto utiliza un autómata finito determinista para clasificar las entradas, un autómata finito no determinista para gestionar el diálogo, una pila para conservar el contexto y un banco finito de respuestas predeterminadas.

Este informe documenta el desarrollo del banco de plantillas, las pruebas ejecutadas y la preparación de la interfaz gráfica.

### 2. Banco de plantillas

El banco de plantillas se encuentra en `plantillas/banco.py` y está implementado mediante la clase `BancoPlantillas`.

Su función es seleccionar respuestas predeterminadas según el estado del chatbot y personalizarlas mediante variables, como el nombre de una película, un actor o un género.

Las respuestas se encuentran organizadas por estados, entre ellos:

- INICIO
- SALUDANDO
- CONVERSANDO
- HABLANDO_PELICULA
- HABLANDO_ACTOR
- HABLANDO_GENERO
- OPINANDO
- PREGUNTANDO
- PROVOCADO
- DESPEDIDA
- FINAL

El banco utiliza selección aleatoria entre las respuestas disponibles. Esto permite ofrecer cierta variedad sin recurrir a inteligencia artificial generativa.

### 3. Personalización de respuestas

Las plantillas pueden incluir el marcador `{tema}`, que se reemplaza por el tema recibido.

Por ejemplo, una plantilla como:

`¿Qué es lo que más te gusta de {tema}?`

puede producir:

`¿Qué es lo que más te gusta de Titanic?`

El banco también puede consultar la pila de contexto mediante el método `peek()` cuando no recibe una entidad explícita.

### 4. Pila de contexto

La pila se encuentra en `pila/contexto.py` y está implementada mediante la clase `PilaContexto`.

Sus operaciones principales son:

- `push(tema)`: agrega un tema.
- `pop()`: retira y devuelve el tema superior.
- `peek()`: consulta el tema superior sin retirarlo.
- `esta_vacia()`: comprueba si existen elementos.

La pila sigue el principio LIFO: el último elemento en entrar es el primero en salir. Esta estructura permite recuperar temas anteriores durante una conversación, siempre que el motor de diálogo solicite las operaciones adecuadas.

### 5. Interfaz gráfica

La interfaz se encuentra en `interfaz.py` y utiliza Tkinter.

Incluye:
- Una ventana principal.
- Un área de conversación.
- Un campo de entrada.
- Un botón para enviar mensajes.
- Una opción para limpiar la conversación.

La interfaz se comunica con la clase `ChatbotCine` mediante el método `procesar_entrada()`.

La interfaz visual se ha probado de forma independiente. La conversación completa todavía requiere integrar el AFD, el AFN, la pila y el banco de plantillas.

### 6. Pruebas realizadas

Se han obtenido los siguientes resultados:

| Componente | Resultado |
|---|---:|
| Pruebas del banco de plantillas | 24/24 aprobadas |
| Pruebas completas del banco | 74/74 aprobadas |
| Pruebas de la pila y las plantillas | 13/13 aprobadas |
| Pruebas del clasificador léxico | 36/36 aprobadas |
| Validación exhaustiva del AFD | 157 autómatas y 7654 secuencias verificadas |

Estos resultados corresponden a las pruebas ejecutadas sobre los componentes individuales y su integración parcial. No demuestran todavía que todas las capas funcionen correctamente en conjunto.

### 7. Preparación de la integración

Se elaboraron dos documentos de apoyo:

- `CONTRATO_INTEGRACION.md`: define las responsabilidades e interfaces previstas entre los componentes.
- `CASOS_PRUEBA_CHATBOT.md`: describe las conversaciones y situaciones que deberán comprobarse cuando el sistema esté integrado.

El motor AFN todavía debe incorporarse para validar el flujo completo de una conversación.

### 8. Conclusión

El banco de plantillas, la pila de contexto y sus pruebas cuentan con una base funcional y documentada. La interfaz gráfica también está preparada para recibir y mostrar mensajes.

El siguiente objetivo es integrar estos componentes con el AFD y el AFN, comprobar el comportamiento del sistema durante conversaciones completas y verificar que las transiciones, las operaciones de contexto y las respuestas coincidan con el diseño del proyecto.
