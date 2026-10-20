
# Casos de prueba — Turing Test Arena: Cine

## Objetivo

Definir las conversaciones que deberán probarse al integrar el AFD, el AFN, la pila de contexto y el banco de plantillas.

Estos casos describen el comportamiento esperado. No se consideran pruebas aprobadas hasta ejecutarlos con el chatbot integrado.

## Caso 1. Saludo inicial

**Entrada:** Hola.

**Token esperado:** SALUDO.

**Comportamiento esperado:**
- El chatbot parte del estado INICIO.
- El AFN selecciona una transición válida.
- La respuesta saluda al usuario e invita a hablar de cine.

## Caso 2. Mención de película

**Entrada:** Me gusta Titanic.

**Token esperado:** MENCION_PELICULA, si así lo determina el AFD.

**Comportamiento esperado:**
- El chatbot reconoce el tema de la película.
- El tema se guarda en la pila cuando corresponda.
- La respuesta hace referencia a Titanic.

## Caso 3. Mención de actor

**Entrada:** Me gusta Tom Hanks.

**Token esperado:** MENCION_ACTOR, si así lo determina el AFD.

**Comportamiento esperado:**
- Se reconoce al actor.
- La respuesta contiene una pregunta o comentario relacionado con él.
- El contexto se conserva según las reglas definidas.

## Caso 4. Mención de género

**Entrada:** Me encantan las películas de comedia.

**Token esperado:** MENCION_GENERO, si así lo determina el AFD.

**Comportamiento esperado:**
- Se reconoce el género.
- La respuesta invita a conversar sobre películas de ese tipo.

## Caso 5. Pregunta

**Entrada:** ¿Qué película me recomiendas?

**Token esperado:** PREGUNTA, si así lo determina el AFD.

**Comportamiento esperado:**
- El AFN selecciona una transición válida.
- El banco produce una respuesta relacionada con la pregunta.

## Caso 6. Opinión

**Entrada:** Esa película es excelente.

**Token esperado:** OPINION, si así lo determina el AFD.

**Comportamiento esperado:**
- El chatbot responde a la opinión.
- La respuesta invita a explicar o ampliar el punto de vista.

## Caso 7. Retomar un tema

**Preparación:** Guardar una película en la pila y después cambiar de tema.

**Entrada:** Volvamos a esa película.

**Token esperado:** RETOMAR_TEMA, si así lo determina el AFD.

**Comportamiento esperado:**
- El chatbot recupera el contexto pertinente.
- La respuesta hace referencia al tema recuperado.
- La pila se modifica solamente según la regla de contexto acordada.

## Caso 8. Entrada desconocida

**Entrada:** No sé qué decir ahora.

**Token esperado:** El que determine el AFD; DESCONOCIDO es una posibilidad.

**Comportamiento esperado:**
- El chatbot no termina inesperadamente.
- Devuelve una respuesta válida que permita continuar la conversación.

## Caso 9. Provocación

**Entrada:** Tu opinión sobre cine es terrible.

**Token esperado:** PROVOCACION, si así lo determina el AFD.

**Comportamiento esperado:**
- El chatbot responde sin abandonar el dominio cinematográfico.
- El AFN aplica una transición válida.

## Caso 10. Despedida

**Entrada:** Adiós.

**Token esperado:** DESPEDIDA.

**Comportamiento esperado:**
- El chatbot muestra una despedida.
- El estado final y la posibilidad de continuar o reiniciar la conversación siguen las reglas definitivas del AFN.

## Caso 11. No determinismo

**Preparación:** Utilizar un estado y token que tengan al menos dos transiciones válidas.

**Comportamiento esperado:**
- El AFN identifica las alternativas válidas.
- Selecciona una mediante un mecanismo aleatorio.
- Nunca selecciona una transición inexistente.

Una sola ejecución no demuestra que la selección sea aleatoria. Debe revisarse también el código de selección.

## Caso 12. Persistencia del contexto

**Preparación:** Guardar dos temas diferentes en la pila.

**Comportamiento esperado:**
- peek devuelve el tema superior sin eliminarlo.
- pop retira el tema superior.
- El tema anterior queda disponible después de retirar el superior.

## Criterio final

Cada caso deberá ejecutarse con el sistema integrado. Se registrarán la entrada, el token, el estado anterior, el estado siguiente, las acciones de pila y la respuesta obtenida.
