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

### 2.4 🔝 Lo que se mide no es "si cambia el número": es la descomposición DENTRO/ENTRE

*(Formulado el 2026-08-20 explicándoselo a G. Es una mejora del diseño, no una aclaración.)*

**Cambiar de escala no es elegir otras unidades: es FUNDIRLAS.** De 36.302 secciones se pasa a 8.131
municipios, y esos 28.171 números que faltan no se han perdido — **se han promediado**. Al fundir,
la variación **dentro** de cada municipio desaparece y solo sobrevive la variación **entre**
municipios.

🔑 **Y ahí está el mecanismo del MAUP, en una frase:** si la relación renta↔ΔVOX **dentro** de los
municipios y **entre** municipios van en direcciones distintas, el resultado cambia de magnitud —o
de signo— sin que ningún dato sea falso.

**Ejemplo de juguete, para tenerlo escrito:** 2 municipios, 4 secciones.

| Municipio | Sección | Renta | Δ VOX | | Municipio | Renta media | Δ medio |
|---|---|---|---|---|---|---|---|
| A | A1 | 10 | +20 | | **A** | 20 | +10 |
| A | A2 | 30 | +0 | | **B** | 40 | **+12** |
| B | B1 | 30 | +22 | | | | |
| B | B2 | 50 | +2 | | | | |

*Lupa fina:* dentro de cada municipio, **más renta → menos crecimiento**. *Lupa gruesa:* el municipio
más rico creció más → **más renta → más crecimiento**. **Mismos datos, titular invertido.**

### Tres consecuencias, y la segunda cambia lo que este trabajo puede reclamar

**1. La pregunta *"¿qué escala es la verdadera?"* está mal planteada.** No hay una. Más fino compra
homogeneidad y **paga en ruido** (una sección son ~1.500 votantes: 40 personas mueven el porcentaje),
en **arbitrariedad de frontera** (§6-bis) y **sigue sin llegar a la persona** — el voto es secreto,
así que el nivel exacto no existe en ningún dato. **La escala correcta la fija la teoría del
mecanismo, no los datos.** Elegir una sin decir por qué es tomar una decisión de fondo a escondidas.

**2. 🔝 Si el signo se da la vuelta, eso NO es un artefacto: es evidencia de DOS mecanismos a dos
niveles.** *"Dentro de un pueblo, VOX crece en los barrios de menos renta"* y *"los pueblos donde más
crece VOX son los de más renta"* **pueden ser ciertas a la vez y no se contradicen** — comparan cosas
distintas. **El MAUP deja de ser un problema a declarar y pasa a ser un instrumento que separa dos
afirmaciones que estaban mezcladas.**

**3. Y eso reencuadra el trabajo entero, a mejor.** Deja de ser *"compruebo si vuestra conclusión
aguanta"* —destructivo, fácil de despachar— y pasa a ser *"vuestra conclusión mezclaba dos
afirmaciones distintas; aquí están separadas"*. **Constructivo, más publicable y mucho más difícil de
rechazar.**

🎯 **Y muerde directo a la diana:** *"a VOX lo trajo la renta media-alta"* no dice **más renta que
quién** — ¿que otros barrios del mismo municipio, o que otros municipios?
⚠️ `[pendiente-verif]` No se ha releído su artículo para confirmar que no lo especifican. **Antes de
afirmarlo, comprobarlo** — es exactamente el error que ya se cometió el 19-ago (§6-bis).

⚠️ `[pendiente-diseño]` La técnica estándar para separar dentro/entre son los **modelos multinivel**
(o meter las medias de grupo como regresor). 🟢 A favor: nuestras cinco escalas son **anidadas de
verdad** (sección ⊂ distrito ⊂ municipio ⊂ provincia ⊂ CCAA), que es el caso limpio para esa familia
de modelos. ⚠️ En contra: **no es una técnica nueva**, así que la novedad no puede apoyarse en ella —
se apoya en aplicarla a esta pregunta, en cinco escalas y con muestra fija. Y **descomposición
multinivel ≠ MAUP completo**: cubre el efecto de escala, no el de zonificación.

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

### 5.6 El lenguaje: Python *(decidido con G, 2026-08-19)*

✅ **El motor de v2 va en Python.** R queda reservado para piezas concretas, si aparecen.

**Y el argumento que decidió NO fue "ya está empezado"** — eso es coste hundido y se descartó
explícitamente aplicando la regla de *"¿qué construirías si el repo estuviera vacío?"*. Con el repo
vacío la cosa estaba **reñida**: en R, buena parte del trabajo del día 3 habría sido
`install.packages("infoelectoral")`, que ya trae lectores de estos ficheros. *(Con dos matices: ese
paquete es una **transcripción a mano** del mismo documento, o sea justo el tipo de suposición no
verificada que mató a v1; y el fallo del delimitador (§7-ter) **solo aparece leyendo la fuente**.)*

Lo que decidió, en orden:

1. 🔑 **Escribo yo, lee G.** Su nivel es equivalente en los dos lenguajes —comprensión media-alta,
   escritura baja—, así que el criterio no es *cuánto cuesta escribir* sino **cuánto cuesta leer**.
   R tiene idiomas propios que hay que conocer (`<-`, fórmulas, `%>%`, la sintaxis de `data.table`);
   Python se lee más literal. Con ese perfil, pesa.
2. **Un idioma, no dos.** Dos entornos, dos gestores de dependencias, dos superficies de rotura en
   Windows. Para un proyecto de una persona y media esa factura se paga entera y no compra nada.
3. **La infraestructura fea ya está probada** (cadena TLS, lector de layout, 15 tests contra datos
   reales). Rehacerla en R obliga a volver a demostrar lo que ya funciona, sin producir nada nuevo.
4. **Lo que falta está cubierto:** `PySAL` para estadística espacial —lo lidera **Luc Anselin**, el
   autor del manual canónico de econometría espacial, así que no es una imitación de R sino la misma
   escuela—, `geopandas` para mapas, `pandas` para tablas.
   ⚠️ `[pendiente-verif]` La atribución de PySAL a Anselin no se ha comprobado contra fuente; se
   comprueba antes de que aparezca en ningún texto publicable.

**Válvula de escape, definida ahora para no improvisarla:** si surge una técnica mal resuelta en
Python, **esa pieza** se hace en R y se comunica con el resto **por fichero plano (CSV)**. Un puente,
no una fusión. Lo mismo aplica a la viñeta para los paquetes de R, si algún día se escribe (§8.3).

**Lo único que daría la vuelta a esto:** que el destinatario prioritario fueran los paquetes de R.
No lo es — G eligió académicos (§8), y a un académico le da igual el lenguaje si el método está
escrito.

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

## 6-bis. 🟢 La mortalidad de secciones: MEDIDA — el diseño aguanta

`[MEDIDO 2026-08-19 con G, código en src/v2/supervivencia_secciones.py, 10 tests]`

**El riesgo de §12.7 —que una sección censal no sobreviva entre convocatorias, y el diseño de §1.2
compare un sitio con otro sitio— era real y estaba sin medir. Ya está medido. NO mata el diseño.**

### Cómo se midió, y por qué el control es la mitad del método

Se compara la lista de secciones de tres convocatorias, sacada del fichero `09` de cada zip
(provincia + municipio + distrito + sección). **Dos comparaciones, no una:**

| | Salto | Para qué |
|---|---|---|
| **Control** | abr-2019 → nov-2019 (6 meses) | En medio año el INE apenas retoca. **Tiene que salir casi perfecto** |
| **Real** | nov-2019 → jul-2023 (3 a. 8 m.) | La pregunta |

🔑 **Sin el control, un resultado raro en la comparación real no se puede atribuir**: no sabrías si
describe el país o describe tu propio error. El control salió **99,92 %**, con 30 muertes y 15
nacimientos — ni un 100 % sospechoso ni ruido. **El instrumento mide lo que dice medir.**

### Y la medida obvia escondía justo el caso peligroso

La supervivencia de **código** salió **99,26 %** — mucho mejor de lo que esperábamos los dos
(predicciones escritas antes: G 90 %, Claude 85-95 %). Pero **nacieron 426 secciones y solo murieron
268**, y esa asimetría tiene una explicación:

> Cuando el INE parte una sección, lo natural es que **una mitad conserve el código del padre** y la
> otra reciba uno nuevo. Para un recuento de códigos esa sección **"sobrevive"** — cuando en realidad
> ha perdido medio cuerpo. **El caso limpio se ve; el sucio es invisible.**

Se detecta pidiendo **dos** condiciones a la vez, porque ninguna vale sola: (a) que el censo caiga
≥30 %, y (b) que en su mismo municipio y distrito **haya nacido** una sección nueva. Solo (a)
confunde partición con **despoblación real**, que en el interior existe y **no es un problema —es el
dato que queremos medir**. Solo (b) no dice a quién se partió.

**Umbral del 30 %: elegido con G y ANTES de mirar.** Se reporta también a otros umbrales para que se
vea que la conclusión no depende de dónde se puso la raya.

### El resultado

| De las 36.302 secciones de nov-2019 | | |
|---|---|---|
| **Intactas** — mismo sitio, comparables | **35.730** | **98,42 %** |
| Particiones ocultas — conservan nombre, no son el mismo sitio | **304** | 0,84 % |
| Muertas — el código desaparece | 268 | 0,74 % |
| Solo encogen — despoblación real, **sin problema** | 17 | 0,05 % |

**Rompen la comparación 572 secciones: el 1,58 %.** Sensibilidad al umbral: 374 ocultas a −20 %, 304
a −30 %, 202 a −40 %, 82 a −50 %. *(Control: 12 ocultas en seis meses — el orden de magnitud correcto
para un método que no inventa particiones donde no las hay.)*

🟢 **Y una consecuencia que descarga el riesgo casi entero:** las piezas de una partición **se quedan
dentro de su distrito y su municipio**. O sea que **el problema solo existe en el peldaño más fino**;
municipio, provincia y CCAA están limpios por construcción.

### Qué se hace con las 572 — decidido con G, en este orden

1. **A · Reconstruir** *(preferido)*: comparar la sección de 2019 con **la suma de sus herederas** en
   2023. ⚠️ **Solo donde el emparejamiento sea único** (un distrito, una muerte, un nacimiento);
   donde haya varias candidatas, se va a C.
2. **C · Apartar y declarar** el resto, **con la lista de cuáles y dónde**. Es la trampa de §6 —
   descartar lo que se movió— pero ahora es del 1,58 % y **caracterizado**, no un tercio y a ciegas.
3. **B · Subir de peldaño** (medir el cambio solo desde municipio) **solo si A y C fallan**: salva el
   diseño **renunciando a la comparación sección↔municipio, que es el producto**.

🔴 **Límite honesto de A, y lo cazó G:** la prueba de que los censos sumen **descarta, no confirma**.
Dos trozos de mapa distintos pueden tener la misma gente dentro. Si `1ºA+1ºB` suman 1.200 donde había
3.000, el emparejamiento está mal **con seguridad**; si suman 3.050, puede estar bien **o haber
cuadrado por casualidad con la madre equivocada**. Confirmarlo de verdad exige **geometría**
(cartografía anual del INE) o **una tabla oficial de correspondencias** — y ninguna de las dos está
verificada (§12.8). **Hasta entonces, A es provisional.**

### ⚠️ ~~Un resultado publicable que no estaba en el plan~~ — DEGRADADO el mismo día

**Lo que se escribió por la mañana:** *"Este número no existía. Nadie ha publicado a qué ritmo se
reescribe la geografía electoral española más fina."*

🔴 **No se sostiene tal cual, y duró cuatro horas.** Al comprobar §12.8 apareció que **Pérez & Pavía
han calculado la estructura de correspondencias de toda España, año a año, de 2001 a 2023**
(§6-ter). Con eso en la mano, derivar cuántas secciones cambian por ciclo electoral es trivial.

**Estado corregido: `[sin verificar si es novedoso]`**, no *"es novedoso"*. No se ha leído su artículo
entero.

🔴 **Y una segunda corrección, del 2026-08-20:** aquí se escribió que *"Roig et al. hacen un salto más
largo (2016→2023) a nivel de sección y no mencionan haberlo tratado"*. **También es falso.** Su
artículo dice literalmente que *"el proceso inferencial comienza alineando las secciones censales
entre distintos momentos temporales"*, citando **Pavía & López-Quílez (2013)** y **Pavía & Cantarino
(2017)**. Lo trataron, con métodos propios. `[verificado 2026-08-20 sobre el texto del artículo]`

🧭 **Y la lección, que vale más que el hallazgo perdido:** la afirmación de novedad se escribió
**antes** de buscar quién lo había hecho. Es la cuarta vez que algo plausible y escrito resulta
falso al comprobarlo, y la primera en que el autor del error fue el mismo turno que lo escribió.
**El orden correcto es buscar primero y afirmar después.**

## 6-ter. 🟢 Cartografía y correspondencias: las dos existen `[VERIFICADO 2026-08-19]`

Comprobación de §12.8, pedida por G. Las dos respuestas son **sí**, y la segunda cambia el plan.

### Cartografía del seccionado — INE, anual, libre

`[verificado contra el propio servidor del INE, no por resumen de búsqueda]`

| | |
|---|---|
| **Servicio** | OGC API-Features · WFS · WMS · descarga Shapefile |
| **Colecciones** | `Secciones_2007` … `Secciones_2025`. **`Secciones_2019` comprobada existente** |
| **Series** | Seccionado del **Censo Electoral (CE)** y del **Padrón (PA)**, 2007→hoy, más los Censos 2001 y 2011 |
| **Atributos** | `CUSEC` (código completo), `CPRO`, `CMUN`, `CDIS`, `CSEC`, `CNUT1-3`, geometría |
| **Coste** | Gratis. Cita obligatoria: «Seccionado cedido por el Instituto Nacional de Estadística» |
| **Punto de entrada** | `https://www.ine.es/geoserver/ogc/features/v1/collections` |

🔑 **`CUSEC` empalma directamente con lo que leemos del fichero `09`**, así que el cruce está resuelto.
Y hacía falta igualmente para el mapa de §4 y para los vecinos de §5.5 — no era solo para el plan A.

⚠️ `[pendiente-verif]` **La fecha de referencia de cada capa anual no está comprobada.** El INE dice
que el seccionado se consolida *"usualmente con referencia al 1 de enero o la fecha de operaciones
estadísticas relevantes"*. Nuestras elecciones son de **noviembre-2019** y **julio-2023**: hay que
comprobar a qué fecha corresponde cada capa antes de dar por buena la correspondencia con el
seccionado electoral del día de la votación.

### La correspondencia entre años: existe, y es mejor que una tabla

**`sc2sc`** — paquete de **R en CRAN** `[verificado: v0.0.1-19, publicado 2026-05-02, cubre 2001-2026]`.
Autores: **Virgilio Pérez y José M. Pavía**. Artículo:
*Automatización de la transferencia de datos entre secciones censales y códigos postales a lo largo
del tiempo. Una aplicación para España* (2024), DOI `10.38191/iirr-jorr.24.057`.

No da un emparejamiento *"esta sección se convirtió en aquella"*. Compara **geométricamente** los
mapas de dos años y calcula **qué proporción del territorio** de cada sección origen va a cada
sección destino. *(Su ejemplo del artículo: el 31,3 % de una sección de 2022 venía de una de 2021 y
el 68,7 % de otra.)* Generan 42 ficheros de correspondencias entre pares de años consecutivos, hacia
delante y hacia atrás.

> 🔑 **Su ejemplo de demostración ES nuestro problema:** datos electorales de Valencia, **2019 contra
> 2023**, 590 → 591 secciones, 5 desaparecen y 6 aparecen, y lo describen como *"rupturas en la serie
> longitudinal de votos que complican las comparaciones"*. **El riesgo de §6-bis queda confirmado por
> terceros independientes**, y con los mismos años.

### Consecuencias, y son tres

1. 🔄 **El plan A de §6-bis queda superado** — emparejar hermanas por censo era una aproximación
   casera y esto es lo mismo hecho bien, con geometría y publicado.
   🔴 **Pero NO se adopta `sc2sc` como calculadora.** *(Corregido el 2026-08-20; el 19-ago se escribió
   aquí "se adopta como vía principal", y estaba mal razonado.)* `sc2sc` reparte **por superficie**,
   lo que equivale a suponer que la gente está repartida uniformemente por el terreno. **Falso**: si
   una sección se parte en un parque y unos bloques de pisos, el reparto 50/50 le regala al parque
   votos que no existen.
   ⚠️ **Y a nosotros ese error nos hace más daño que a un usuario normal, por cómo está montado el
   diseño:** medimos **el cambio**, así que un error de estimación **no se ve como ruido, se ve como
   crecimiento**. En un estudio de niveles un error es ruido; en uno de cambios, es un resultado
   falso. Además el error **no es aleatorio**: las particiones ocurren donde ha crecido la población
   —periferias, obra nueva—, un tipo de sitio muy concreto.

   ✅ **Lo que se hace en su lugar, decidido con G:**
   - **Fusionar hasta cerrar.** Si `S1` se partió en `S1`+`S2`, se comparan como **una sola unidad**
     en los dos años. No se estima nada: es una suma. Si además entró territorio de un vecino `S3`,
     **se mete `S3` entero en los dos años**, y así hasta que el trozo esté cerrado —nada entró, nada
     salió—. **Siempre se llega**; en el peor caso al municipio, que no se mueve.
     🔑 **La exactitud siempre está disponible. Lo que se paga por ella es resolución.**
   - **`sc2sc` como DETECTOR, no como calculadora.** Sus proporciones dicen si un caso está limpio
     (todo el territorio va a un sitio, ratio = 1) o sucio (0,31 / 0,69). O sea: se usa para saber
     **cuándo no hace falta estimar**. Uso más humilde y mucho más sólido.
   - **`sc2sc` como prueba de robustez al final:** *"sale lo mismo fusionando y con el método de
     Pavía"* es más fuerte que elegir uno de los dos.

   ⚠️ **Contrapeso, y no es menor:** fusionar mete, en el peldaño más fino, **unas cuantas unidades
   más gruesas** — y el tamaño de la unidad **es literalmente la variable que se estudia**. Hay que
   comprobar que esas 572 no ensucian la comparación entre escalas. `[pendiente-diseño]`
2. 🔴 **Cuarto camino independiente que lleva a Pavía** (§8): coautor de la diana, mantenedor del
   SEA, destinatario, y ahora autor de la herramienta que resuelve nuestro problema. **Deja de ser
   una coincidencia y pasa a ser un dato sobre el campo**: este nicho lo ocupa un grupo.
3. ⚠️ **`sc2sc` es R.** Es el **primer uso de la válvula de escape de §5.6**, abierta menos de una
   hora antes: esa pieza se ejecuta en R y se comunica por CSV. **La decisión de Python aguanta
   porque la válvula estaba prevista** — pero conviene registrar que hizo falta enseguida.

## 7. Lo demás que está sin resolver

| # | Qué | Estado |
|---|---|---|
| 1 | ~~La descarga oficial no verifica TLS~~ | ✅ **RESUELTO el 2026-08-17** con verificación completa. Y el diagnóstico que había aquí era **falso**: ver §7-bis |
| 2 | El **layout** de los ficheros de ancho fijo | ✅ **RESUELTO el 2026-08-18.** La especificación viaja DENTRO del zip (`FICHEROS.doc`) y ahora se lee **desde código**: `src/v2/layout_infoelectoral.py`. Y al contrastarla con los ficheros reales apareció que **la especificación miente en una frase**: ver §7-ter |
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

## 7-ter. El layout, leído — y la frase de la especificación que es falsa

`[VERIFICADO 2026-08-18, con código que corre y 15 tests]` El layout ya no se supone: se lee.
`src/v2/lector_doc.py` abre el `FICHEROS.doc` (binario OLE2 de Word 97) **en Python puro**, y
`src/v2/layout_infoelectoral.py` lo convierte en un esquema con **los 12 tipos de fichero y sus
campos**. Ninguna posición está escrita a mano en el repo: si el Ministerio cambia la
especificación en una convocatoria futura, el esquema cambia solo.

🔴 **Y la especificación se equivoca en su primer párrafo.** Dice que los registros van *"con
delimitador de registro CR+LF"*. **Es falso**: los diez `.dat` de 2019-11 no contienen **ni un
solo `\r`**. El delimitador es `LF` a secas.

> **No es una pega de estilo.** Un lector que se crea esa frase y descuente dos bytes por registro
> se desplaza **un byte por línea**, y a partir del segundo registro lee todos los campos corridos
> — con cifras que **siguen pareciendo cifras**. Es exactamente el modo de fallo silencioso que la
> regla *"se lee, no se supone"* existe para evitar… salvo que aquí **leer la especificación no
> bastaba**. Hacía falta contrastarla contra el fichero.
>
> 🧭 Es la tercera vez en este proyecto que un enunciado plausible y escrito resulta falso al
> comprobarlo (los otros dos: el diagnóstico del certificado, §7-bis; y el dataset `renta`, §7.6).

**Lo que sí encaja, y se comprueba en cada test:** los diez ficheros de datos del zip `MESA`
tienen registros de **exactamente** la longitud que declara la especificación —25, 40, 232, 120,
233, 33, 172, 33, 101 y 36 bytes—, **todos** sus campos numéricos traen dígitos, y el fichero de
control `01` declara qué ficheros se adjuntan **coincidiendo con lo que hay dentro del zip**.

⚠️ **`antiword` no se usa aunque está instalado en esta máquina.** Extrae el `.doc` bien, y sirvió
para contrastar la implementación mientras se escribía — pero es un binario de mingw que no está
en Linux, ni en CI, ni en la máquina de quien replique esto. **Misma lección que §7-bis: lo que
funciona en la máquina de uno no es lo que funciona.**

### 7-ter-bis. 🔴 Y el peldaño "distrito" no es un peldaño de verdad

`[MEDIDO 2026-08-18 sobre el fichero 09 de 2019-11]` Al contar las unidades de cada escala:

| Escala | Unidades (generales 2019-11, sin C.E.R.A.) |
|---|---|
| Sección censal | **36.302** |
| Distrito | **10.485** |
| Municipio | **8.131** |

> 🔑 **Solo 1.091 de los 8.131 municipios (13,4 %) tienen más de un distrito.** En el 86,6 %
> restante el distrito **es literalmente el municipio**, con otro código.

Consecuencia para §3, y no es cosmética: la escalera **no tiene cinco peldaños comparables**.
Comparar *distrito* con *municipio* es comparar dos cosas idénticas en 7 de cada 8 unidades, y
donde se diferencian —las ciudades grandes— la comparación **describe la España urbana y solo
esa**. O se declara así, o el peldaño se retira. **Sin decidir; se decide con G.**

*(El 8.131 sirve además de control externo: es el mismo número de municipios que usó eldiario.es
en su análisis de julio de 2023, §8. La lectura del fichero cuadra con una fuente independiente.)*

## 8. Quién actúa distinto (criterio de impacto) — resuelto, y no donde se suponía

✅ **PRIORIDAD DECIDIDA POR G el 2026-08-19: los académicos primero.** Y no obliga a renunciar a
nada, porque **el análisis es común a los cuatro destinatarios** —los cuatro quieren el mismo
número— y lo único que cambia es el envoltorio final. La asimetría que justifica el orden: **de un
trabajo que aguanta escrutinio académico sale gratis la nota periodística; al revés no.** La única
consecuencia temprana es el idioma, y por eso se decidió a la vez (§9.4).

⚠️ **Contrapeso, que va escrito para que no se olvide:** *"lo más exigente primero"* es también la
forma clásica de no terminar nunca. Sigue mandando §5.3.1 — **el primer corte tiene que valer solo.**

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

## 8-bis. 🟢 ¿Nos están pisando? Barrido del grupo de Pavía `[2026-08-20]`

Comprobación de §12.12, la del riesgo competitivo. **No hay señal de que hayan hecho la pregunta de
escala** — y el motivo es más interesante que el resultado.

**Su línea viva 2025-2026 es inferencia ecológica, entera:** *A Bottom-Up Approach for Ecological
Inference* · *Ecological Inference for Electoral Analysis* · *Estimating Vote Transition Counts* ·
*EcolRxC* · *From Corrado Gini's Early Contributions to Overdispersion…*

**Y su obra espacial va toda en la misma dirección, que no es la nuestra:**

| Trabajo | Qué resuelve |
|---|---|
| Pavía & López-Quílez (2013), *JRSS-A* 176(3):655-678 | Redistribuir votos cuando **redibujan** las unidades → el eje del **tiempo** |
| Pavía & Cantarino (2017a,b), *Geographical Analysis* 49(2) y *Applied Geography* 86 | Repartir mejor **dentro** de una unidad (mapeo dasimétrico) |
| `sc2sc` (2024/2026) | Transferir estadísticas **entre años** |

> 🔑 **Todo su aparato sirve para MOVER datos entre unidades. Ninguna pieza pregunta si la respuesta
> cambia según el TAMAÑO de la unidad.** Tienen las herramientas y no han hecho la pregunta — que es
> justamente el hueco de §2.1.

⚠️ **Límite del barrido, declarado:** es un repaso de listas de publicación, **no exhaustivo**. No
cubre preprints, congresos ni trabajo en curso. Es evidencia de ausencia débil, no prueba.

### 🟢 Y algo que juega a favor: ellos mismos declaran la limitación de `sc2sc`

En las conclusiones de su propio artículo escriben que *"al usar únicamente la superficie implicada y
no considerar cómo se distribuye la población dentro del territorio, algunas imputaciones —
especialmente los recuentos— podrían mejorarse significativamente"*, y proponen incorporar **técnicas
dasimétricas con datos catastrales**.

**Es exactamente la objeción del "problema del parque" (§6-ter).** No es una crítica externa ni
ingenua: **es la limitación que los propios autores declaran**. Refuerza la decisión de usar `sc2sc`
como detector y no como calculadora, y da una forma cortés de plantearlo.

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

- ✅ **DECIDIDO POR G el 2026-08-19: bilingüe desde ya.** Era una consecuencia razonada; ahora es una
  decisión tomada. Marginal si se hace desde el principio, caro y mal hecho si se traduce al final.
  **Reparto exacto**, para que no haya que volver a preguntarlo:

  | Qué | Idioma |
  |---|---|
  | El **producto** (primer corte, figuras, texto de resultados) | **Bilingüe ES/EN** |
  | Los **documentos de diseño internos** (este, la referencia core) | **Español** |
  | La **conversación de trabajo y las explicaciones a G** | **Español**, siempre |
  | Términos técnicos sin traducción decente (*MAUP*, *ecological inference*…) | **Inglés**, definidos en español la primera vez que aparecen |

  *(G tiene C1: el inglés no es una barrera, es una cuestión de velocidad de lectura. Lo que se pueda
  en español, en español.)*
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

---

## 12. 🔴 LO QUE ESTÁ SIN VERIFICAR — la lista, en un sitio

Cada uno de estos avisos está también en su sección, pero **repartidos por un documento largo se
pierden**. Esta es la lista corta.

**La regla que los gobierna, y ya ha cobrado dos víctimas:** el 17-ago cayeron dos candidatos al
comprobarlos — uno porque **ya estaba hecho**, y otro porque **una cita correcta sostenía una inferencia
falsa**. Y un tercero se salvó por poco: el diagnóstico del certificado (§7-bis) era plausible, estaba
escrito en cuatro ficheros, y era falso.

> **Comprobar antes de apoyarse. Y antes de presentar, no después.**

| # | Qué está sin verificar | Por qué importa | Coste | §  |
|---|---|---|---|---|
| 1 | **¿Ha cruzado alguien SERPAVI con datos electorales?** | Si está ocupado, deja de ser la fuente diferencial y pasa a ser una más | ~20 min | §5.2 |
| 2 | **¿Hasta qué año llega el Censo Anual** (estudios, edad, nacionalidad) **a sección censal?** | Si no cubre el periodo, **no se puede prometer serie larga** con esas variables — y son las que la literatura dice que pesan más que la renta | ~20 min | §5.2 |
| 3 | **¿Dónde crece VOX de verdad?** El argumento del riesgo de muestra (§6) supone que crece en el rural diminuto | 🔴 **Es una de las cosas que este trabajo va a MEDIR.** No puede darse por sabida de entrada ni usarse como premisa | Sale del propio análisis | §6 |
| 4 | **Cerrar la búsqueda de novedad en Dialnet y TESEO a texto completo** | Una tesis o un TFM español podría haber hecho ya el análisis multiescala. **El barrido del 17-ago no los cubrió** | ~1 h | §2.2 |
| 5 | **El vínculo capitales ↔ maniobra de cohesión** (Varsovia, Budapest) | Está verificado que la maniobra existe y que esas regiones salen en los datos; **no que cada caso concreto sea el mismo** | Cruzar región a región con fechas de revisión de la nomenclatura | §9.3 |
| 6 | **Las coaliciones de VOX**: en qué convocatorias y territorios concurrió coaligado | Decide qué candidaturas cuentan. **Se escribe antes de mirar los datos** | Sale de los propios ficheros | §5.1 |
| 7 | ~~**¿Sobrevive una sección censal entre dos convocatorias?**~~ | ✅ **MEDIDO el 2026-08-19 → §6-bis. NO mata el diseño.** 98,42 % de las secciones son comparables tal cual; rompen la comparación 572 (1,58 %), de las cuales **304 lo hacían de forma invisible**. Y el problema **vive solo en el peldaño más fino** | — | §6-bis |
| 8 | ~~**¿Publica el INE cartografía anual de secciones y/o una tabla de correspondencias?**~~ | ✅ **COMPROBADO el 2026-08-19 → §6-ter. Las dos existen.** Cartografía anual del INE 2007-2025, libre, con `CUSEC`. Y `sc2sc` en CRAN (Pérez & Pavía) da correspondencias **geométricas con proporciones**, 2001-2026. **El plan A queda superado por algo mejor** | — | §6-ter |
| 12 | ~~**¿Ha hecho ya el grupo de Pavía la pregunta de ESCALA?**~~ | 🟢 **BARRIDO el 2026-08-20 → §8-bis. No hay señal.** Su línea 2025-2026 es **inferencia ecológica** entera; su obra espacial (Pavía & López-Quílez 2013; Pavía & Cantarino 2017; `sc2sc`) sirve para **mover datos entre unidades**, nunca para preguntar si la respuesta cambia con el tamaño de la unidad. **Tienen las herramientas y no han hecho la pregunta.** ⚠️ Barrido de listas de publicación, no exhaustivo: no cubre preprints ni congresos | — | §8-bis |
| 13 | 🆕 **Sánchez-García & Llamazares (2025)** — VOX en secciones censales metropolitanas | Citados **dentro** de la diana: hallan que VOX crece en suburbios **con crecimiento de población, renta más baja y más paro** (*left-behind*) — **dirección contraria** a la conclusión de Roig et al. **No verificado de primera mano**, solo por cómo lo citan otros | Localizar y leer: ~1 h | §2.3 |
| 10 | 🆕 **¿Publican Pérez & Pavía la tasa de cambio del seccionado**, o solo las correspondencias? | Decide si nuestra cifra de §6-bis (304 particiones ocultas, 98,42 % estable) es un resultado o una redundancia. **No se ha leído su artículo entero** | Leer el artículo: ~1 h | §6-bis |
| 11 | 🆕 **¿A qué fecha corresponde cada capa anual de cartografía del INE?** | El INE consolida *"usualmente a 1 de enero"*, y nuestras elecciones son de nov-2019 y jul-2023. Si las capas no coinciden con el seccionado del día de la votación, la correspondencia se desalinea | ~30 min | §6-ter |
| 9 | 🆕 **¿Por qué contamos 36.460 secciones en jul-2023 y eldiario.es habla de ~35.500?** | Casi mil de diferencia. Puede ser redondeo suyo, otra fuente (mapa del INE vs fichero electoral) o un filtro. **No se da por resuelto** | ~20 min | §6-bis, §8 |

⚠️ **Y uno que no es de este repo pero condiciona lo que se cita:** el material de investigación del que
salió parte de este diseño **no tiene pase verificador independiente** (141 marcas pendientes). Sus
conclusiones cualitativas orientaron bien; **sus cifras no son citables sin abrir la fuente**.

**Ninguno de estos bloquea el trabajo de mañana** — salvo, quizá, el 7. Lo que bloquean los otros es
**publicar** o **presentar** apoyándose en ellos. La diferencia importa: se puede construir con una
incógnita declarada; no se puede afirmar con ella.

🆕 **El 7 es de otra clase y por eso va aparte:** los seis primeros son cosas que hay que *comprobar
antes de afirmar*. El 7 es una **tensión entre dos decisiones ya tomadas**, y si sale mal no obliga a
matizar un párrafo sino a **cambiar el diseño**. Se levantó el 2026-08-18 al transcribir el layout y
**está sin discutir con G**: aquí solo queda anotado, no resuelto.
