# Documentación técnica: Banco de respuestas

## 1. Objetivo

El banco de respuestas es el componente encargado de proporcionar mensajes predeterminados al chatbot de cine. Su propósito es mantener una conversación coherente mediante respuestas asociadas a los estados del sistema, sin utilizar inteligencia artificial generativa.

## 2. Organización de las respuestas

Las plantillas están almacenadas en la clase `BancoPlantillas`, dentro del archivo `plantillas/banco.py`. Se organizan según los estados definidos para el chatbot:

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

Cada estado dispone de una o varias respuestas predeterminadas.

## 3. Selección de respuestas

El método `obtener()` recibe el estado actual, el token léxico, la pila de contexto y una posible entidad detectada. A partir de estos datos selecciona una respuesta mediante una elección aleatoria entre las opciones disponibles.

También existen respuestas específicas para determinadas combinaciones de estado y token.

## 4. Personalización del contenido

Las plantillas utilizan la variable `{tema}` para incorporar información relevante, como el nombre de una película, un actor o un género cinematográfico.

Por ejemplo, una respuesta puede mencionar directamente *Titanic* o *Tom Hanks*. Si no se proporciona una entidad válida, el banco intenta recuperar el tema de la pila de contexto y, si no está disponible, utiliza una referencia genérica.

## 5. Validación y manejo de errores

El banco incorpora el método `validar_plantillas()`, que comprueba la existencia de respuestas para los estados definidos y revisa el formato de las plantillas.

Además, contempla estados desconocidos, temas vacíos y errores de formato para evitar interrupciones innecesarias.

## 6. Pruebas realizadas

Se ejecutaron las siguientes pruebas:

- Pruebas iniciales del banco: 24 de 24 aprobadas.
- Validación del archivo y ejemplos de respuestas: correcta.
- Pruebas ampliadas del banco: 74 de 74 aprobadas.
- Pruebas del clasificador léxico: 36 de 36 aprobadas.
- Pruebas de los autómatas: 157 AFD y 7654 secuencias verificadas.

Los resultados corresponden a las ejecuciones realizadas durante el desarrollo. La integración completa del chatbot deberá verificarse por separado.

## 7. Conclusión

El banco de respuestas cuenta con plantillas organizadas por estado, selección aleatoria, personalización mediante variables y mecanismos de validación. Su diseño permite conectarlo con el clasificador léxico, el motor de diálogo y la pila de contexto cuando la integración de estos componentes esté disponible.