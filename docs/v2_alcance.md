# v2 — Alcance: qué es este proyecto y qué no

> **Estado:** vivo · **Decidido:** 2026-08-16 · **Arrancado:** 2026-08-17 (`deaa81e`)
> Sustituye al diseño europeo anterior, que se ejecutó y resultó inviable. Ver §5.

---

## 1. La pregunta

> **¿Dónde y por qué crece el voto a partidos de ámbito no estatal (PANE) en España — y cambia la
> respuesta según la escala territorial a la que se mire?**

Las dos mitades no pesan igual. **La segunda es el producto.**

## 2. Por qué la escala es el producto y no un chequeo

El mismo dato puede contar una historia agregado por municipios y otra distinta agregado por
provincias. No es un detalle técnico: es un resultado conocido en geografía cuantitativa —el
*modifiable areal unit problem*— y significa que **elegir el nivel de agregación es tomar una decisión
sustantiva sin declararla**.

Casi todo lo que se publica sobre voto territorial en España elige un nivel (normalmente provincia,
porque es el que se tiene a mano) y no comprueba si la conclusión sobrevive a cambiar de nivel.

Aquí sí se comprueba, y con **cuatro escalas reales**: mesa → municipio → provincia → comunidad
autónoma. Si el signo o la magnitud cambian entre ellas, ese es el hallazgo. Si no cambian, también:
es una afirmación de robustez que hoy nadie puede hacer.

## 3. La segunda mitad del producto: el mapa que se niega a pintar

Un mapa coloreado transmite certeza uniforme aunque la evidencia debajo no lo sea. Aquí:

- donde la muestra o la cobertura no sostienen una estimación, **se pinta gris y se dice por qué**;
- cada número arrastra su procedencia;
- la incertidumbre se enseña, no se resume.

Es deliberadamente lo contrario del incentivo estético normal de un panel.

## 4. Decisiones de diseño ya tomadas

### 4.1 El objeto se define por dónde concurre un partido, no por lo que piensa

**PANE = partido de ámbito no estatal**: categoría establecida en la ciencia política española, y
definida por su **implantación territorial**, no por ideología.

Esto es una decisión de medida, no de vocabulario. Etiquetar un partido como "nacionalista" es un
juicio interpretativo, está disputado, y en la práctica **las bases académicas que lo hacen dejan sin
veredicto justo a los partidos españoles relevantes**. La condición de ámbito no estatal, en cambio,
**se calcula desde los propios resultados electorales**: en cuántas circunscripciones concurre.

🔴 **Pendiente y con regla:** el umbral operativo exacto (¿cuántas circunscripciones?, ¿sobre qué
convocatorias?) **se escribe ANTES de mirar los datos**. Un umbral elegido después de ver el resultado
no es un criterio, es una conclusión disfrazada.

### 4.2 Las fuentes

| Capa | Fuente | Nivel más fino | Estado |
|---|---|---|---|
| Electoral | **Infoelectoral** (Ministerio del Interior) | **mesa** | 🔴 bloqueada: ver §6 |
| Socioeconómica | Por decidir — **INE** (ARDECO no baja de NUTS3) | por comprobar | ⏳ sin resolver |

### 4.3 Dos condiciones que no se negocian

1. **El primer corte tiene que valer solo.** Si nada de lo que venga después llega a existir, el
   trabajo hecho hasta ese punto debe seguir siendo defendible por sí mismo. En cuanto se añada una
   pieza *"porque hará falta más adelante"*, parar.
2. **La diferenciación va dentro del primer corte, no después.** Un mapa con una regresión es trabajo
   replicable en semanas por cualquiera. Lo que no lo es son las cuatro escalas y la capa de
   honestidad. Si eso se aplaza, no hay proyecto: hay un mapa más.

## 5. Qué NO hace este proyecto

- **No hace dashboard.** No es una herramienta de exploración libre: un panel donde se cruzan decenas
  de variables a voluntad es una máquina de producir correlaciones espurias.
- **No hace clustering ni tipologías.**
- **No predice elecciones.** Esa es una línea distinta y opcional, y solo tendría sentido **después**,
  reutilizando esta capa como tubería.
- **No depende del modelo de medida ESS**, que está congelado por una solución factorial impropia.

## 6. Lo que está sin resolver ahora mismo

| # | Qué | Por qué bloquea |
|---|---|---|
| 1 | 🔴 **La descarga oficial no verifica TLS.** El certificado de Infoelectoral es auténtico pero lo emite la **FNMT-RCM**, que no está en el almacén de raíces de Mozilla → ni en Python ni en `certifi` | Sin resolverlo no hay datos. **La salida es añadir la raíz, NO desactivar la verificación**: bajar datos oficiales por un canal sin verificar invalidaría la procedencia, que es la mitad del valor de esto |
| 2 | El **layout** de los ficheros de ancho fijo del Ministerio | Hay que leer la especificación oficial. **Suponer una estructura no verificada es exactamente lo que mató a v1** |
| 3 | La **fuente socioeconómica municipal** | Sin ella, media pregunta no se puede responder |
| 4 | **Quién usa esto.** No está resuelto quién haría algo distinto en su trabajo porque este análisis exista | Es el punto débil declarado del proyecto. Un hallazgo de escala debería cambiar cómo alguien elige el nivel al que publica un mapa — falta confirmarlo con un caso real |

## 7. Por qué murió el diseño anterior (v1), para no repetirlo

v1 era europeo y comparado: resultados electorales europeos × economía regional × clasificaciones
académicas de partidos. **Se ejecutó**, y el resultado fue que no era viable con esas fuentes:

1. la base electoral europea **no baja de NUTS2** — no existía la escala fina que el diseño pedía;
2. en España **el 22,9 % del voto se quedaba sin veredicto de partido**, y eran precisamente los de
   ámbito no estatal: **la cobertura era peor justo donde estaba el objeto**;
3. el identificador común de partido **no señala al mismo partido entre fuentes** — verificado a mano,
   con falso positivo y falso negativo a la vez.

**Murieron las fuentes, no la pregunta.** Los tres motivos empezaban por *"porque esa base…"*.
Cambiándolas, los tres desaparecen por construcción: la escala la da el Ministerio, el objeto se
calcula desde los propios resultados, y no hay identificador que cruzar.

> El código de v1 (`src/join_economico_electoral.py`, `src/cobertura_partidos.py`,
> `src/ingestion/load_euned.py`) se conserva porque **es la prueba de todo lo anterior**, pero está
> fuera del camino de v2. No construir encima sin releer esta sección.
