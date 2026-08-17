# v2 — Alcance: qué es este proyecto y qué no

> **Estado:** vivo · **Decidido:** 2026-08-16 · **Arrancado:** 2026-08-17 (`deaa81e`)
> **Revisado a fondo el 2026-08-17** con dos barridos de verificación. Varias cosas de la primera
> versión de este documento eran optimistas de más y están corregidas abajo, marcadas.
> Sustituye al diseño europeo anterior, que se ejecutó y resultó inviable. Ver §8.

---

## 1. La pregunta

> **¿Dónde y por qué crece el voto a partidos de ámbito no estatal (PANE) en España — y cambia la
> respuesta según la escala territorial a la que se mire?**

Las dos mitades no pesan igual. **La segunda es el producto.**

## 2. Por qué la escala es el producto — y qué se puede reclamar de verdad

El mismo dato puede contar una historia agregado por secciones censales y otra por municipios. No es
un detalle técnico: es un resultado conocido —el *modifiable areal unit problem*, MAUP— y significa
que **elegir el nivel de agregación es tomar una decisión sustantiva sin declararla**.

### 2.1 Lo que se puede afirmar, y lo que NO

🔴 **La aportación es de APLICACIÓN, no de invención. Decirlo así desde el primer párrafo.**

- **No** se puede vender como *"descubro que la escala importa"*. La pieza canónica es de hace un año:
  **Lee, Rogers & Soifer (2025), *The Modifiable Areal Unit Problem in Political Science*, Political
  Analysis 33(4)** — en simulación, **~1/3 de los pares de mapeados espaciales dan resultados
  inconsistentes**, con signos de coeficiente que cambian de forma impredecible. Cubre EE.UU. y Reino
  Unido, **no España**.
- **Sí** se puede afirmar esto, que es más honesto y sigue siendo publicable:
  > **En la literatura electoral española el MAUP se cita como coartada y no se mide nunca.** Los
  > trabajos lo invocan para justificar que usan la unidad más fina disponible — y ahí se acaba.
  > Aquí está la medida.

### 2.2 Antecedentes que hay que citar de entrada, no esperar a que los saque un revisor

| Trabajo | Qué hizo | Qué deja libre |
|---|---|---|
| **Maza & Hierro (2022)**, *A polarization approach to Catalonia's independence case*, Economia Politica 39:323-344 | 🔴 **El competidor más cercano.** Tratan el MAUP **explícitamente** sobre voto independentista municipal | Resolvieron la **zonificación** (cómo dividir dentro de la unidad). **Nadie ha hecho la ESCALA** (comparar entre niveles). **Esa distinción es lo que salva la novedad** |
| *The emergence of the radical right…* (2025, Andalucía, VOX, 778 municipios) | Nombra el MAUP para justificar usar municipio | No compara escalas |
| Roig, Espinosa & Pavía (2025), *Who votes for Vox?*, Frontiers in Political Science 7 | Sección censal + renta del ADRH | Una sola escala; ni nombra el MAUP |
| Iglesias-Pascual et al. (2022), Spatial Demography | Durbin espacial, sección censal | Una sola escala |
| Sánchez-Díaz et al. (2020), *PUEM y enfermedades raras*, Investigaciones Geográficas 74 | 🟢 **MAUP hecho en España de verdad**: provincia/comarca/municipio | Objeto sanitario, **cero datos electorales**. Es una **plantilla metodológica directa** |

⚠️ **Límites del barrido**, declarados: ScienceDirect devolvió 403 varias veces (3-4 referencias vistas
por snippet, no a texto completo) y **no se buscó en Dialnet/TESEO a texto completo** — una tesis o un
TFM español podría haberlo hecho. **Antes de publicar, cerrar esa búsqueda.**

## 3. La escalera de escalas — CORREGIDA

🔴 **La versión inicial decía "mesa → municipio → provincia → CCAA". Está mal: no hay datos
socioeconómicos a nivel de mesa.** La fuente económica (ADRH) baja hasta sección censal y ahí para.

**Escalera real, con dato en los dos lados:**

```
sección censal  →  distrito  →  municipio  →  provincia  →  CCAA
```

Cinco peldaños. El nivel de **mesa** queda fuera del diseño: Infoelectoral sí lo da, pero no hay con
qué cruzarlo.

🔝 **Y el blanco cambia: el frente vivo es SECCIÓN CENSAL vs MUNICIPIO.**
La primera versión apuntaba a los mapas provinciales. **Era un muñeco de paja**, por dos razones:
(a) el periodismo de datos español ya se bajó a sección censal hace años; (b) los mapas provinciales
que quedan son de **reparto de escaños**, donde la provincia **es la circunscripción legal** y no una
agregación arbitraria. Donde la elección sí es arbitraria — y donde **los mismos equipos alternan sin
justificarlo** — es entre sección censal y municipio.

## 4. La otra mitad del producto: el mapa que se niega a pintar

Un mapa coloreado transmite certeza uniforme aunque la evidencia debajo no lo sea. Aquí: donde la
cobertura no sostiene una estimación **se pinta gris y se dice por qué**, cada número arrastra su
procedencia, y la incertidumbre se enseña en vez de resumirse.

## 5. Decisiones de diseño

### 5.1 El objeto: PANE — y una corrección al entusiasmo inicial

**PANE = partido de ámbito no estatal**, definido por su **implantación territorial** (en cuántas
circunscripciones concurre), no por ideología. Frente a etiquetar un partido como "nacionalista"
—juicio interpretativo, disputado, y que en las bases académicas dejaba sin veredicto justo a los
partidos españoles relevantes— la condición de ámbito no estatal **se calcula desde los propios
resultados electorales**.

🔴 **PERO: esto disuelve el juicio ideológico, NO el problema de identidad de partido.** La primera
versión de este documento decía que "los tres motivos desaparecen por construcción". **Era demasiado
fuerte.** Infoelectoral da **códigos de candidatura que cambian entre convocatorias**, sin
identificador estable de partido. Concretamente:

- ✅ **Dentro de una convocatoria**, la condición PANE es observable sin ambigüedad: en qué
  circunscripciones aparece esa candidatura, y se lee del propio fichero.
- 🔴 **Entre convocatorias**, enlazar "la misma fuerza política" **vuelve a ser trabajo manual** — que
  es exactamente lo que hundió a v1. Coaliciones que cambian de nombre, marcas que se fusionan.

**Regla que se adopta:** el análisis principal es **de corte transversal, por convocatoria**, donde el
problema no existe. Cualquier panel entre años declara el enlace como **decisión documentada y
falible**, con su tabla de correspondencias publicada. **No se arrastra el problema en silencio.**

🔴 **Pendiente y con regla:** el umbral operativo exacto que define PANE **se escribe ANTES de mirar
los datos**. Un umbral elegido después de ver el resultado no es un criterio, es una conclusión
disfrazada.

### 5.2 Las fuentes — verificadas contra la API del INE, no de memoria

| Capa | Fuente | Nivel más fino | Años | Estado |
|---|---|---|---|---|
| Electoral | **Infoelectoral** (Mº Interior) | mesa (con distrito y sección) | 1976→ | 🔴 descarga bloqueada, ver §7 |
| Socioeconómica | **INE — Atlas de Distribución de Renta de los Hogares (ADRH)**, operación 353 | **sección censal** | **2015-2023** | ✅ verificado |

**Qué da el ADRH** `[verificado vía API]`: renta neta y bruta media por persona y por hogar, media y
mediana por unidad de consumo, **índice de Gini**, **P80/P20**, distribución por fuente de ingreso, y
% de población bajo umbrales de pobreza por sexo/edad/nacionalidad. Fuente: IRPF de la AEAT **y de las
Haciendas Forales de País Vasco y Navarra** → **PV y Navarra sí están cubiertos**, lo que importa
mucho aquí porque son casos centrales del objeto.

**Cobertura temporal:** 2015-2023 cubre las generales de 2015, 2016, 2019 (×2) y 2023. Sin huecos.

⚫ **El paro NO sirve a escala fina.** SEPE y Seguridad Social enmascaran las celdas <5, y **el SEPE
cambió la política a mitad de serie** (2013 trae números reales, 2025 ya no). En municipios pequeños
los desgloses son mayoritariamente inutilizables y la serie está rota. **La renta del ADRH es la
variable económica robusta; el paro no.**

### 5.3 Dos condiciones que no se negocian

1. **El primer corte tiene que valer solo.** Si nada de lo que venga después llega a existir, lo hecho
   hasta ahí debe seguir siendo defendible. En cuanto se añada una pieza *"porque hará falta más
   adelante"*, parar.
2. **La diferenciación va dentro del primer corte.** Un mapa con una regresión es replicable por
   cualquiera en semanas. Lo que no lo es son las cinco escalas y la capa de honestidad.

## 6. 🔴 EL RIESGO QUE MATA EL DISEÑO (no la ejecución)

**El ADRH omite las unidades de menos de 100 habitantes.** Consecuencia:

> **La muestra de unidades CAMBIA con la escala.** A nivel de sección censal se caen unas unidades, a
> nivel municipal otras, a nivel provincial ninguna. Si estimas el mismo modelo a cinco escalas sobre
> **cinco muestras distintas**, no puedes saber si el coeficiente se movió **por la agregación** o
> **por qué territorios entraron y salieron**.

**Y el sesgo no es aleatorio: los municipios diminutos del rural interior son justo donde vive el voto
regionalista.** O sea que apunta contra el objeto del estudio.

**Mitigación obligatoria, no opcional:**
1. **Fijar la muestra** a las unidades presentes en **todas** las escalas.
2. **Reportar por separado** el efecto de selección, como resultado propio.

**Si esto no se hace, el estudio no identifica nada.**

> 🧭 **Y esto ya había pasado antes.** E0 encontró exactamente la misma forma de trampa: *"los huecos
> entre escalas no son simétricos y sesgan en una dirección — las regiones sin dato eran sobre todo
> capitales; comparar escalas sin cuadrar muestra atribuiría a la escala la desaparición de la
> capital."* **Es el mismo error reapareciendo en un diseño nuevo.** Que se haya visto a tiempo dos
> veces no significa que se vea sola la tercera.

## 7. Lo demás que está sin resolver

| # | Qué | Estado |
|---|---|---|
| 1 | 🔴 **La descarga oficial no verifica TLS.** El certificado de Infoelectoral es auténtico pero lo emite la **FNMT-RCM**, que no está en el almacén de raíces de Mozilla → ni en Python ni en `certifi`. **La salida es añadir la raíz, NO desactivar la verificación**: bajar datos oficiales por un canal sin verificar invalidaría la procedencia | 🟢 **Pista:** los paquetes de R `infoelectoral` y `pollspain` **ya descargan de ahí**. Mirar cómo lo resuelven es más corto que buscar la raíz a ciegas |
| 2 | El **layout** de los ficheros de ancho fijo | Leer la especificación oficial. **Suponer estructura no verificada es lo que mató a v1** |
| 3 | **Códigos incompatibles**: los del Ministerio del Interior **no** son los del INE. Y la correspondencia de secciones censales entre ficheros cartográficos, electorales y padronales *"no siempre coincide"* y *"varía en el tiempo"* (documentado por el proyecto SEA) | Existen tablas de correspondencia mantenidas en el paquete `infoelectoral` |
| 4 | **Fronteras de sección censal que cambian cada año** | Paradójicamente es *material* para un estudio de MAUP —es el efecto de zonificación puro— pero hay que tratarlo explícitamente |
| 5 | 🟡 **Volumen**: la API del INE rechaza descargas completas del ADRH por restricción de volumen; el CSV masivo sí funciona pero una tabla pesa ~352 MB | Manejable, pero no es un `read_csv` inocente |
| 6 | ⚠️ **Trabajo previo que puede reducir el esfuerzo — o parte del espacio**: el **SEA (Spanish Electoral Archive)**, en Harvard Dataverse, fusiona resultados + cartografía + padrón desde mesa hasta CCAA (generales 1979-2019). Y el paquete `infoelectoral` **ya trae un dataset `renta`** con >34.000 filas cruzando renta del INE por sección censal | **Revisarlo antes de escribir una línea de fontanería.** Puede ahorrar semanas — o mostrar que parte de esto ya está hecho |

## 8. Quién actúa distinto (criterio de impacto) — resuelto, y no donde se suponía

**No es la academia de PANE**: sus trabajos usan encuestas individuales del CIS/CEO, así que **no
eligen nivel de agregación** y el criterio no les aplica. Es **periodismo de datos** y **metodología
espacial**.

| Quién | Por qué actuaría distinto |
|---|---|
| 🔝 **Raúl Sánchez** y **Victòria Oliveres** (unidad de Datos, eldiario.es) | Publicaron **la misma pregunta a dos escalas con dos días de diferencia**: voto PANE × renta sobre **8.131 municipios** (23-jul-2023) y voto × renta sobre **35.500 secciones censales** (25-jul-2023). El matiz de por qué eso importa está en su propia metodología, **sin cuantificar** |
| **Kiko Llaneras** (El País) | Renta × voto independentista por sección censal; ya avisa contra la lectura ecológica y la trata a mano. Un Δ por escala le da la magnitud que hoy no tiene |
| **Borja Andrino** (El País) | Afirma por escrito que *"el voto nacionalista es más fuerte en los municipios pequeños"* — que es literalmente el enunciado que este trabajo pone a prueba |
| **José M. Pavía** y **Virgilio Pérez** (Univ. de València, GIPEyOP) | Su obra entera es transferencia de votos entre unidades areales cambiantes. Es su terreno y no lo han medido para PANE |
| **Toni Rodon** (UPF), **Marc Guinjoan** (UAB), **Jordi Muñoz** (UB) | Eligieron nivel municipal teniendo comarcas disponibles, sin justificarlo, y ya detectaron de refilón sensibilidad al tamaño |
| **Javier Álvarez-Liébana** (`pollspain`) y **Héctor Meleiro** (`infoelectoral`) | Sus paquetes ofrecen elegir el nivel territorial **sin ninguna guía de qué cambia al cambiarlo**. Una viñeta sobre eso es adopción inmediata |

## 9. Qué NO hace este proyecto

- **No hace dashboard.** Un panel donde se cruzan decenas de variables a voluntad es una máquina de
  correlaciones espurias.
- **No hace clustering ni tipologías.**
- **No predice elecciones.** Esa es una línea distinta y opcional, y solo tendría sentido **después**.
- **No depende del modelo de medida ESS**, congelado por una solución factorial impropia.

## 10. Por qué murió el diseño anterior (v1), para no repetirlo

v1 era europeo y comparado. **Se ejecutó**, y no era viable con esas fuentes:

1. la base electoral europea **no baja de NUTS2**;
2. en España **el 22,9 % del voto se quedaba sin veredicto de partido**, y eran precisamente los de
   ámbito no estatal — **la cobertura era peor justo donde estaba el objeto**;
3. el identificador común de partido **no señala al mismo partido entre fuentes**.

**Murieron las fuentes, no la pregunta.** Cambiándolas, (1) se resuelve del todo y (2) también; (3)
**se reduce pero no desaparece** — ver §5.1.

> El código de v1 (`src/join_economico_electoral.py`, `src/cobertura_partidos.py`,
> `src/ingestion/load_euned.py`) se conserva porque **es la prueba de todo lo anterior**, pero está
> fuera del camino. No construir encima sin leer esta sección.
