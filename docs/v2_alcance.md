# v2 — Alcance: qué es este proyecto y qué no

> **Estado:** vivo · **Decidido:** 2026-08-16 · **Arrancado:** 2026-08-17 (`deaa81e`)
> **Revisado a fondo el 2026-08-17**, tres veces y en este orden: dos barridos de verificación externa,
> y una **redefinición del objeto y del diseño** al final del día. Varias cosas de las primeras
> versiones eran optimistas de más o estaban mal argumentadas; **están corregidas en su sitio y
> marcadas**, no añadidas encima.
>
> 🔝 **Los dos cambios grandes, por si vienes de una versión anterior:** el objeto pasó de *"partidos de
> ámbito no estatal"* a **VOX** (§1.1), y el diseño pasó de medir el **nivel** en una elección a medir
> el **cambio** entre elecciones (§1.2). Los dos los propuso G y los dos mejoran el proyecto.
>
> Sustituye al diseño europeo anterior, que se ejecutó y resultó inviable. Ver §11.

---

## 1. La pregunta

> **¿Dónde ha CRECIDO el voto a VOX en España entre elecciones — y cambia la respuesta según la escala
> territorial a la que se mire?**

Las dos mitades no pesan igual. **La segunda es el producto.**

### 1.1 El objeto es VOX, y no "partidos de ámbito no estatal" *(cambiado el 2026-08-17)*

La primera versión de este documento medía el voto a **PANE** (partidos de ámbito no estatal). Se
cambió, y el motivo es de fondo, no de gusto.

🔴 **Agregar PANE rompe la variable dependiente.** Euskadi y Cataluña están **por encima** de la media
española de renta; Galicia y Canarias, **por debajo**. Meterlas en el mismo saco y preguntar *"¿se vota
más nacionalismo donde hay menos renta?"* **promedia mecanismos contrarios que se cancelan**. Y no es
solo económico: son trayectorias históricas distintas —fueros, Renaixença, Rexurdimento, insularidad—
que no comparten ni origen ni cronología. Un promedio de fenómenos contrarios no significa nada.

**Y una corrección a lo que este documento decía antes**, porque estaba mal argumentado: se afirmaba
que "nacionalista" es *"un juicio ideológico discutible"*. **Para el núcleo de partidos es un hecho, no
una etiqueta externa** — el PNV se declara nacionalista en sus propios estatutos y el BNG lo lleva en el
nombre. El problema real era otro, y son tres cosas distintas:

1. 🔑 **"Nacionalista" a secas incluye a VOX**, que es nacionalista **español**. La categoría que se
   quería nombrar es **nacionalismo *periférico***; sin ese apellido, PNV y VOX caen en la misma bolsa.
2. **Los bordes son grises de verdad**: Coalición Canaria, Teruel Existe, PAR, UPN, Compromís.
3. **Las coaliciones se mueven** entre convocatorias (CiU → PDeCAT/Junts; coaliciones mixtas con
   partidos estatales), y enlazar "la misma fuerza política" entre años **es trabajo manual** — que es
   exactamente lo que hundió a v1.

**Qué gana el diseño con un partido único:**

| | |
|---|---|
| **Clasificación** | Desaparece entera. Un partido, un código, sin bordes ni coaliciones que resolver. **El riesgo que mató a v1 se evapora, esta vez del todo** |
| **Homogeneidad** | Un discurso y una campaña nacional. No se suman cuatro historias distintas |
| **Cobertura** | Concurre en toda España → hay variación en todo el territorio, no en cuatro esquinas. **Muchas más unidades para la pregunta de escala** |
| **Diana** | La literatura reciente sobre VOX **es exactamente lo que este trabajo pone a prueba** (§2.2) |

⚫ **PANE queda como CONTRASTE opcional**, no como saco: comparar si el efecto de escala es **mayor en
un voto muy concentrado territorialmente** que en uno repartido. Segundo resultado casi gratis con la
misma tubería — **y lo primero que se cae si aprieta el tiempo.**

### 1.2 Se mide el CAMBIO, no el nivel *(cambiado el 2026-08-17)*

**"Auge" es un cambio, no una foto.** La pregunta no es *dónde saca VOX más voto*, sino **dónde ha
crecido más**.

🔑 **Y esto solo es posible con un partido estable** — VOX existe desde 2013 con las mismas siglas. Con
PANE no se podía: las marcas se rompen y se fusionan entre convocatorias y nunca sabes si comparas lo
mismo. **El cambio de objeto desbloqueó el cambio de diseño.**

**Y es metodológicamente más sólido, no solo más cercano a la pregunta.** Comparando sitios entre sí,
cualquier diferencia puede venir de mil cosas no medidas: historia, industria, estructura de edad,
cultura política. Comparando **el mismo sitio consigo mismo en dos momentos**, todo lo que no cambia
**se resta solo** y queda únicamente lo que se movió.

> Es la diferencia entre *"los altos pesan más que los bajos"* y *"esta persona ha engordado"*. La
> segunda es mucho más difícil de discutir.

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

### 2.2 🔝 LA DIANA — Roig, Espinosa & Pavía (2025)

`[LEÍDO A TEXTO COMPLETO el 2026-08-17, no solo el resumen]`
**"Who votes for Vox? Socioeconomic profiles and electoral shifts in the region of Madrid"**,
*Frontiers in Political Science* 7:1717586.

| | |
|---|---|
| **Fuentes** | 🔑 **Las mismas dos que este proyecto**: resultados a sección censal (vía **SEA**) + **Atlas de renta del INE (ADRH)** |
| **Periodo** | 2016 → 2023. Generales de abr-19, nov-19 y jul-23, más autonómicas de Madrid |
| **Método** | **Inferencia ecológica** con el algoritmo `rslphom` — matrices de transferencia de voto, sin encuesta |
| **Hallazgo** | **Contraintuitivo:** la entrada y primera expansión de VOX en Madrid la lideraron votantes de renta **media y alta** —desertores del PP y de Ciudadanos—, **no los de renta baja**. Los *"perdedores de la modernización"* solo se incorporan **después del COVID**. → **Desmienten el marco estándar** |

🔑 **Y aquí está la bisagra de todo este proyecto.** Justifican usar la sección censal **por su
homogeneidad interna** — *"trabajar con unidades espaciales pequeñas ofrece varias ventajas analíticas
frente a niveles más agregados como los municipios"*. Su método, la inferencia ecológica, **descansa
entero sobre ese supuesto**: deducir cómo votan las *personas* mirando datos de *zonas* solo funciona si
la gente de dentro se parece.

> **El MAUP es exactamente lo que rompe ese supuesto. Y no lo mencionan ni una vez.**
>
> Su conclusión más llamativa —*"a VOX lo trajo la renta media-alta"*— **nunca se ha sometido a la
> prueba de cambiar de unidad.**

**Los cuatro huecos — y DOS los piden ellos mismos en su trabajo futuro:**

| Hueco | Origen | ¿Se puede cerrar? |
|---|---|---|
| *"Incorporar medidas explícitas de **desigualdad** junto a la renta, para separar sus efectos"* | **Suyo.** Su renta y su desigualdad correlacionaban **0,47** y no pudieron distinguir cuál manda | ✅ El ADRH ya trae **Gini** y **P80/P20**. Es la columna que les faltó |
| *"Herramientas espaciales que tengan en cuenta las características de las secciones **vecinas**"* | **Suyo** | ✅ Ver §5.5 |
| **La escala** | 🔑 **Su omisión, no su petición** | ✅ **Es el producto de este trabajo** |
| **Madrid → España** | Su alcance declarado | ✅ Por defecto |

🔴 **Encuadre obligatorio, y no es cosmético.** Si esto se presenta como *"analizo el voto a VOX"*, es
replicarles con menos medios y se pierde. **La frase de apertura es siempre la escala:**

> *"Un trabajo de 2025 concluye que a VOX lo trajo la renta media-alta. Su método depende de que las
> unidades sean homogéneas por dentro. Aquí se comprueba si esa conclusión sobrevive al cambiar de
> unidad — y se añaden las dos cosas que sus propios autores pidieron."*

### 2.3 Los demás antecedentes, que también hay que citar

| Trabajo | Qué hizo | Qué deja libre |
|---|---|---|
| **Maza & Hierro (2022)**, *A polarization approach to Catalonia's independence case*, Economia Politica 39:323-344 | 🔴 **El competidor metodológico más cercano.** Tratan el MAUP **explícitamente** sobre voto independentista municipal | Resolvieron la **zonificación** (cómo dividir dentro de la unidad). **Nadie ha hecho la ESCALA** (comparar entre niveles). **Esa distinción es lo que salva la novedad** |
| *The emergence of the radical right…* (2025, Andalucía, **VOX**, 778 municipios) | **Nombra el MAUP** para justificar usar municipio | **Y no compara escalas.** Nombrar el problema y no medirlo es el patrón que este trabajo documenta |
| Iglesias-Pascual et al. (2022), Spatial Demography | Durbin espacial, sección censal, extrema derecha en el sur | Una sola escala |
| Sánchez-Díaz et al. (2020), *PUEM y enfermedades raras*, Investigaciones Geográficas 74 | 🟢 **MAUP hecho en España de verdad**: provincia/comarca/municipio | Objeto sanitario, **cero datos electorales**. Es una **plantilla metodológica directa** |

> 🧭 **Los tres trabajos recientes sobre VOX eligen un nivel y ninguno comprueba si su conclusión
> aguanta al cambiarlo.** Uno de ellos incluso nombra el problema. Ese patrón **es** el hallazgo que
> justifica este proyecto.

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

### 5.1 El objeto: el voto a VOX

Ver §1.1 para el porqué del cambio. Aquí, lo operativo.

**La variable dependiente es el voto a la candidatura de VOX**, identificada por su código de
candidatura en cada convocatoria. Es un partido, no una categoría: **no hay nada que clasificar, ni
bordes que defender, ni coaliciones que resolver.**

⚠️ **Lo único que hay que comprobar, y es mecánico:** VOX ha concurrido en coalición en algunas
convocatorias y territorios. Hay que decidir **por escrito y antes de mirar** si esas candidaturas
cuentan, y con qué regla. Es un puñado de casos, no un problema de fondo — pero se declara igual.

🔴 **DECISIÓN PENDIENTE, y no es menor: ¿voto sobre qué?**

| | Sobre **votos emitidos** | Sobre **censo** |
|---|---|---|
| Qué mide | Cuota entre los que fueron a votar | Capacidad de movilizar sobre el total con derecho a voto |
| Riesgo | Si otros se quedan en casa, VOX "sube" **sin ganar un solo votante** | Mezcla dos cosas: convencer y movilizar |

**Y contamina directamente la pregunta de escala:** la participación **varía sistemáticamente con el
tamaño del municipio** (en pueblos pequeños se vota más). Si se elige mal, parte del "efecto de escala"
será **efecto de participación disfrazado**.
✅ **Lo limpio: calcular las dos y publicar las dos.** Cuesta una columna.

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

#### 🆕 SERPAVI — la fuente que encaja de forma casi absurda `[VERIFICADO 2026-08-17]`

**Sistema Estatal de Referencia del Precio del Alquiler de Vivienda** (Ministerio de Vivienda).

| | |
|---|---|
| **Niveles** | 🔑 **sección censal · distrito · municipio · provincia · CCAA** — **exactamente los cinco peldaños de §3** |
| **Origen** | Datos fiscales reales de alquiler + bases catastrales, explotados por la AEAT |
| **Volumen / años** | >**2,5 M** de alquileres al año · **2011-2023** |
| **Acceso** | Descarga libre en tabla, además de visores cartográficos |

**Por qué suma sobre la renta, y son tres cosas distintas:**
1. **Cubre 2011** en vez de 2015 → **dos convocatorias generales más** para medir crecimiento, que es
   justo lo que necesita el diseño de §1.2.
2. **Mide otra cosa.** La renta dice lo que ingresas; el alquiler, **lo que cuesta vivir ahí**. Un
   barrio puede tener renta media y alquileres asfixiantes. Esa presión de vivienda es un motor
   conocido del voto de derecha radical y **el Atlas de renta no la capta**.
3. **Es una tercera señal de origen distinto**, que ayuda a desenredar el lío renta↔desigualdad que
   Roig et al. declararon no haber podido separar (§2.2).

⚠️ **SIN COMPROBAR: si alguien ya lo ha cruzado con datos electorales.** Es un sistema reciente y Roig
et al. no lo usan, pero **ausencia en una búsqueda no es prueba**. Comprobación pendiente antes de
presentarlo como hueco.

#### Y las variables que probablemente hacen más falta que la renta

En la literatura sobre voto a la derecha radical, **la renta no suele ser el predictor más fuerte**:
suelen serlo el **nivel de estudios**, la **estructura de edad** y el **porcentaje de población
extranjera**. Un modelo solo con renta se arriesga a un resultado flojo — y a que el primer revisor
pregunte por qué faltan.

🟢 Están en el **Censo Anual de Población del INE, a sección censal**. ⚠️ **Su cobertura temporal es más
corta que la del ADRH** (nivel de estudios y actividad, ~2021-2024): **hay que comprobar hasta dónde
llega antes de prometer una serie larga con ellas.**

### 5.3 Dos condiciones que no se negocian

1. **El primer corte tiene que valer solo.** Si nada de lo que venga después llega a existir, lo hecho
   hasta ahí debe seguir siendo defendible. En cuanto se añada una pieza *"porque hará falta más
   adelante"*, parar.
2. **La diferenciación va dentro del primer corte.** Un mapa con una regresión es replicable por
   cualquiera en semanas. Lo que no lo es son las cinco escalas y la capa de honestidad.

### 5.4 🔴 El límite honesto: "dónde" NO es "por qué"

La pregunta que motiva esto es *por qué crece VOX*. **El diseño contesta dónde, no por qué**, y conviene
tenerlo escrito antes de empezar para no cruzar la raya al escribir los resultados.

Aunque salga que VOX creció más donde bajó la renta, **eso admite al menos tres explicaciones
incompatibles**: que gente empobrecida votara VOX; que en esos sitios se marchara gente que votaba otra
cosa; o que renta y voto se muevan juntos porque ambos dependen de un tercer factor no medido.

Tiene nombre: **falacia ecológica** — concluir cosas sobre *personas* mirando datos de *zonas*. *"En las
secciones de menos renta se vota más a VOX"* **no significa** *"los pobres votan VOX"*: puede ser gente
acomodada viviendo en zonas que se empobrecieron.

🔴 **No se arregla con más datos: es una limitación del tipo de dato.** Lo que se hace es **declararlo**
y no cruzar la raya. Y de paso es la mejor defensa ante quien quiera leer el resultado en clave
partidista: si alguien acusa al trabajo de decir que los pobres votan VOX, ya está escrito que eso no se
puede afirmar con estos datos.

**Lo que sí se puede afirmar** —y es el producto—: *la relación entre economía y voto a VOX es de este
tamaño, y se mueve así al cambiar la unidad territorial con la que se mide.*

> 🧭 Y esto muerde con fuerza a la diana de §2.2: la **inferencia ecológica** es, literalmente, el
> intento de saltarse esta limitación. Cuanto más grande es la unidad, menos se sostiene el salto.

### 5.5 Autocorrelación espacial: obligatoria, no opcional

Las unidades vecinas se parecen entre sí. Eso rompe el supuesto de independencia que asumen las
herramientas estadísticas estándar, y hace que **los márgenes de error salgan más pequeños de lo que
deberían**: se aparenta más seguridad de la que hay.

Tiene tratamiento conocido y hay que usarlo. **Y aquí importa más que de costumbre por dos motivos:**
1. **Cuánto se parecen los vecinos también cambia con la escala** — está enredado con la pregunta
   principal, así que ignorarlo contamina el resultado que se quiere medir.
2. **Es una de las dos cosas que Roig et al. piden por escrito** en su trabajo futuro (§2.2).

## 6. 🔴 EL RIESGO QUE MATA EL DISEÑO (no la ejecución)

**El ADRH omite las unidades de menos de 100 habitantes.** Consecuencia:

> **La muestra de unidades CAMBIA con la escala.** A nivel de sección censal se caen unas unidades, a
> nivel municipal otras, a nivel provincial ninguna. Si estimas el mismo modelo a cinco escalas sobre
> **cinco muestras distintas**, no puedes saber si el coeficiente se movió **por la agregación** o
> **por qué territorios entraron y salieron**.

**Y el sesgo no es aleatorio.** Las unidades que se caen son las diminutas del rural interior — y ahí
**el voto a VOX no es un residuo**: parte de su crecimiento más fuerte está justamente en zonas rurales
y en municipios pequeños del interior y del sureste. O sea que **la selección apunta contra el objeto**,
igual que apuntaba cuando el objeto era otro. *(⚠️ Esa afirmación sobre dónde crece VOX es
`[pendiente-verif]`: se apoya en la descripción general del fenómeno, no en una medición propia. Es
además **una de las cosas que este trabajo va a medir**, así que no puede darse por sabida de entrada.)*

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
| 1 | ~~La descarga oficial no verifica TLS~~ | ✅ **RESUELTO el 2026-08-17** con verificación completa. Y el diagnóstico que había aquí era **falso**: ver §7-bis |
| 2 | El **layout** de los ficheros de ancho fijo | ✅ **La especificación viaja DENTRO del zip** (`FICHEROS.doc`, 284 KB, en los tres ámbitos). No hay que buscarla fuera ni suponer nada. Extraída a `data/external/infoelectoral/especificacion/`. **Falta transcribirla a un esquema** |
| 3 | **Códigos incompatibles**: los del Ministerio del Interior **no** son los del INE. Y la correspondencia de secciones censales entre ficheros cartográficos, electorales y padronales *"no siempre coincide"* y *"varía en el tiempo"* (documentado por el proyecto SEA) | Existen tablas de correspondencia mantenidas en el paquete `infoelectoral` |
| 4 | **Fronteras de sección censal que cambian cada año** | Paradójicamente es *material* para un estudio de MAUP —es el efecto de zonificación puro— pero hay que tratarlo explícitamente |
| 5 | 🟡 **Volumen**: la API del INE rechaza descargas completas del ADRH por restricción de volumen; el CSV masivo sí funciona pero una tabla pesa ~352 MB | Manejable, pero no es un `read_csv` inocente |
| 6 | ⚠️ **Trabajo previo**: el **SEA (Spanish Electoral Archive)** y el dataset `renta` del paquete `infoelectoral` | ✅ **REVISADO el 2026-08-17** → [`v2_trabajo_previo.md`](v2_trabajo_previo.md). **El hueco sigue abierto y lo declaran abierto sus dueños.** El SEA **no cruza renta con voto** —su único cruce es con el padrón, y de una sola convocatoria— y el dataset `renta` **se descarta con cifras**: sin año, clave no única (207 códigos con dos valores distintos) y **falta Álava** |

## 7-bis. El bloqueo de la descarga: resuelto, y el diagnóstico anterior era falso

`[VERIFICADO 2026-08-17, con código que corre]` La descarga oficial funciona **con verificación TLS
completa**. Pero antes de eso hay una corrección que conviene no tapar, porque el error tenía forma
de conclusión razonable.

**Lo que decía este documento y el resto del repo:** *"el certificado lo emite la FNMT-RCM, que no
está en el almacén de raíces de Mozilla → ni en Python ni en `certifi`"*.

**Es falso, y se comprueba en una línea:** `certifi` **sí** trae dos raíces de la FNMT — `AC RAIZ
FNMT-RCM` y `AC RAIZ FNMT-RCM SERVIDORES SEGUROS`. La CA española lleva años en el programa de
Mozilla. El síntoma era real; la causa atribuida, no.

**Lo que pasa de verdad** se ve pidiéndole la cadena al servidor:

```
$ openssl s_client -connect infoelectoral.interior.gob.es:443 -showcerts
 0 s:CN=*.interior.gob.es
   i:C=ES, O=FNMT-RCM, OU=AC Componentes Informáticos
Verify return code: 21 (unable to verify the first certificate)
```

**El servidor manda solo el certificado de hoja y omite la intermedia** `AC Componentes
Informáticos`. Es un fallo de configuración del servidor del Ministerio, no un problema de raíces: el
ancla ya es de confianza, lo que falta es el eslabón intermedio. Los navegadores lo tapan porque
bajan solos ese eslabón de la URL que el propio certificado declara en su extensión **AIA**
(*Authority Information Access*); OpenSSL —y por tanto Python, `requests` y `curl`— **no hacen eso**.
De ahí que la fuente se abra en el navegador y no desde código.

**La salida, en `src/v2/cadena_confianza.py`:** se baja la intermedia de la URL del AIA, se
**verifica su firma contra las raíces que ya trae `certifi`**, y se guarda versionada en `certs/`.
El `SSLContext` sale con `CERT_REQUIRED` + `check_hostname`.

> **Confianza nueva añadida: ninguna.** Es importante que la diferencia se vea, porque lo que decía
> este documento —*"añadir la raíz de la FNMT al bundle"*— **sí** habría sido añadir un ancla de
> confianza nueva por decisión propia. Completar una cadena cuyo ancla ya está avalada por Mozilla es
> una operación estrictamente más débil, y por eso mejor.

**Tres controles, y los tres tienen que pasar** (`src/v2/test_cadena_confianza.py`, 7 tests):
firma válida contra una raíz de `certifi`, huella SHA-256 fijada, y validez temporal. Hay un test que
fabrica un impostor **con el subject y el issuer correctos** y comprueba que se rechaza — porque un
módulo de seguridad validado solo con el caso bueno está sin validar. Y un test de política que lee
el AST del módulo y falla si aparece cualquier forma de desactivar la verificación.

⚠️ **Una trampa que casi se cuela, anotada para no repetirla:** el contexto TLS **por defecto** de
Python en Windows sí conecta con Infoelectoral. Es tentador quedarse ahí y declararlo resuelto. Pero
funciona por un motivo que no es reproducible: Windows tenía la intermedia **cacheada en el almacén
del usuario** (`CurrentUser\CA`) de alguna visita previa con navegador. En otra máquina, en Linux o
en CI, ese mismo código falla. **Lo que funciona en la máquina de uno no es lo que funciona.**

🟢 **Y el atajo que había escrito aquí ya no hace falta:** mirar cómo resuelven esto los paquetes de
R `infoelectoral` y `pollspain` era una pista sensata, pero el problema resultó ser más simple que
ir a leer código ajeno. Siguen siendo relevantes por el punto 6, no por este.

**Lo que se comprobó de paso, y no estaba escrito:**

- **Los tres ámbitos publicados no son tres conjuntos de datos.** Comparados entrada por entrada con
  SHA-256: `TOTA` ⊂ `MUNI` ⊂ `MESA`. El ámbito no cambia el catálogo de candidaturas ni de
  candidatos; solo **añade** ficheros de resultados más finos. **Con bajar `MESA` sobra** — una
  descarga en vez de tres, y ninguna duda sobre cuál de las tres copias de un catálogo es la buena.
- **El patrón de nombre de fichero queda comprobado**, no supuesto: `02<año><mes>_<ÁMBITO>.zip`
  descarga los tres ámbitos de 2019-11.

## 8. Quién actúa distinto (criterio de impacto) — resuelto, y no donde se suponía

**No es la academia que estudia estos partidos con encuestas**: sus trabajos usan microdatos
individuales del CIS/CEO, así que **no eligen nivel de agregación** y el criterio no les aplica. Es
**periodismo de datos** y **metodología espacial** — y, desde el 17-ago, **los propios autores de la
diana**.

| Quién | Por qué actuaría distinto |
|---|---|
| 🔝🔝 **Rosa Roig, Priscila Espinosa y José M. Pavía** — autores de la diana (§2.2) | Su conclusión sobre VOX descansa en un supuesto de homogeneidad interna **que nunca han puesto a prueba cambiando de unidad**. Este trabajo la somete a esa prueba **y les entrega las dos cosas que pidieron** (desigualdad junto a renta; herramientas espaciales). Es lo más cerca que hay de un destinatario que **tiene que responder** |
| 🔝 **Raúl Sánchez** y **Victòria Oliveres** (unidad de Datos, eldiario.es) | Publicaron **la misma pregunta a dos escalas con dos días de diferencia**: voto × renta sobre **8.131 municipios** (23-jul-2023) y sobre **35.500 secciones censales** (25-jul-2023). El matiz de por qué eso importa está en su propia metodología, **sin cuantificar** |
| **Kiko Llaneras** (El País) | Renta × voto por sección censal; ya avisa contra la lectura ecológica y la trata a mano. Un Δ por escala le da la magnitud que hoy no tiene |
| **Borja Andrino** (El País) | Afirma por escrito que *"el voto nacionalista es más fuerte en los municipios pequeños"* — un enunciado sobre tamaño de unidad × voto, que es literalmente lo que este trabajo pone a prueba |
| 🔝 **José M. Pavía** y **Virgilio Pérez** (Univ. de València, GIPEyOP) | Su obra entera es transferencia de votos entre unidades areales cambiantes. **Y además mantienen el SEA** `[verificado 17-ago]`, cuyo dataset cruza el voto con el padrón pero **no con la renta** — que su propio artículo declara pendiente de integrar. **El interlocutor, el trabajo previo y la diana son la misma gente**, por tres caminos independientes |
| **Toni Rodon** (UPF), **Marc Guinjoan** (UAB), **Jordi Muñoz** (UB) | Eligieron nivel municipal teniendo comarcas disponibles, sin justificarlo, y ya detectaron de refilón sensibilidad al tamaño |
| **Javier Álvarez-Liébana** (`pollspain`) y **Héctor Meleiro** (`infoelectoral`) | Sus paquetes ofrecen elegir el nivel territorial **sin ninguna guía de qué cambia al cambiarlo**. Una viñeta sobre eso es adopción inmediata |

## 9. El ensanche europeo — verificado, y NO es para ahora

Esto **no entra en el MVP**. Se escribe aquí porque decide cómo se redacta el primer corte, y porque
es la razón de que este trabajo no acabe siendo solo un estudio local.

### 9.1 En Europa, la escala a la que se mide decide quién cobra

`[VERIFICADO 2026-08-17]` La política de cohesión de la UE clasifica **regiones NUTS2** por PIB per
cápita frente a la media europea, y reparte según el umbral:

| Categoría | Umbral | Consecuencia |
|---|---|---|
| Menos desarrollada | **< 75 %** | **El grueso de los fondos** |
| Transición | 75-90 % | |
| Más desarrollada | > 90 % | |

Es decir: **dónde cae la frontera de la región determina de qué lado del umbral cae, y por tanto
cuánto dinero recibe.** El MAUP deja de ser un problema metodológico y pasa a ser un problema de
reparto.

### 9.2 Y ya se ha explotado a propósito

`[VERIFICADO]` Está documentado que **separar las ciudades capitales de sus regiones NUTS2 dio ventaja
a algunos Estados miembros** en el reparto de fondos, con modificaciones hechas por **Hungría, Polonia
y Lituania** que **afectaron a la asignación del periodo 2021-2027**.

### 9.3 🧭 Y el trabajo previo de este repo ya topó con la huella, sin saber qué era

E0 registró esto como una anomalía de cobertura:

> *"Las 22 NUTS2 sin dato de educación son regiones nacidas de revisiones de frontera, sobre todo
> **capitales** (Varsovia, Budapest, Sajonia). Comparar escalas sin cuadrar muestra atribuiría a la
> escala la desaparición de la capital."*

**Varsovia es Polonia. Budapest es Hungría.** Dos de los tres países señalados en §9.2. El código topó
con **la huella en los datos de una maniobra deliberada de reparto** y la anotó como un hueco.

⚠️ El vínculo es **fuerte pero es una hipótesis**: se ha verificado que la maniobra existe y que esas
regiones aparecen en los datos, no que cada caso concreto sea el mismo. **Antes de afirmarlo, cruzar
región a región con las fechas de revisión de la nomenclatura.**

### 9.4 Qué implica para el MVP

- **Se escribe el primer corte en bilingüe desde el principio.** Marginal si se hace ya, caro si se
  hace al final.
- **Se incluye una sección corta sobre el caso europeo**, apuntando a esto, sin ejecutarlo.
- **El artefacto 2**, si lo hay, es apuntar el mismo aparato a NUTS2 y a los umbrales de cohesión.
  Ahí el interlocutor deja de ser una redacción y pasa a ser la Comisión y el Tribunal de Cuentas
  Europeo. **No antes de tener el primer corte entregado.**

## 9-bis. Descartado tras comprobarlo: el experimento de percepción de mapas

Se consideró añadir un experimento aleatorizado — enseñar los mismos datos a dos niveles de agregación
y medir si la gente concluye cosas distintas. Habría convertido un hallazgo técnico en uno sobre
personas, y encima es barato y preregistrable.

🔴 **Está ocupado.** Existe *"Where Maps Lie: Visualization of Perceptual Fallacy in Choropleth Maps at
Different Levels of Aggregation"* (2022) y trabajo reciente en CHI (2024) sobre cómo cambian las
conclusiones del lector según tipo y detalle del mapa. **Se descarta.**

Se anota para que no se vuelva a proponer dentro de tres semanas como si fuera una idea nueva.

## 10. Qué NO hace este proyecto

- **No hace dashboard.** Un panel donde se cruzan decenas de variables a voluntad es una máquina de
  correlaciones espurias.
- **No hace clustering ni tipologías.**
- **No predice elecciones.** Esa es una línea distinta y opcional, y solo tendría sentido **después**.
- **No depende del modelo de medida ESS**, congelado por una solución factorial impropia.

## 11. Por qué murió el diseño anterior (v1), para no repetirlo

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
