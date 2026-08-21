# EU_REFERENCIA_CORE — eu-political-observatory
> Cargado automáticamente por `get_session_context(project="eu_observatory")`.
> Metodología ESS completa: `docs/EU_REFERENCIA.md`.
> **Última actualización: 2026-08-17.**

---

## 🔝 LO PRIMERO: qué es este proyecto AHORA (v2, decidido el 2026-08-16)

**Pregunta:** ¿dónde ha **CRECIDO el voto a VOX** en España entre elecciones — y **cambia la respuesta
según la escala territorial a la que mires**?

Esa segunda mitad **es el producto**, no un chequeo: el mismo dato puede contar una historia agregado
por secciones censales y otra por municipios (*modifiable areal unit problem*). Junto a ella va la
**capa de honestidad**: un mapa que **se niega a pintar** donde no hay base y lo dice.

🔝 **Dos cambios del 17-ago por la tarde, que hay que respetar** (detalle en §1.1 y §1.2 del alcance):
- **El objeto es VOX, no PANE.** Agregar Euskadi/Cataluña (renta alta) con Galicia/Canarias (renta baja)
  **promedia mecanismos contrarios y rompe la variable**. Con un partido único desaparece además todo el
  problema de clasificación — el que mató a v1. PANE queda como **contraste opcional**, no como saco.
- **Se mide el CAMBIO entre elecciones, no el nivel en una.** "Auge" es un cambio, y **solo es posible
  con un partido estable**. Comparar el mismo sitio consigo mismo resta lo que no cambia.

🎯 **Y hay diana con nombre:** Roig, Espinosa & Pavía (2025), *Frontiers in Political Science* — **usan
las mismas dos fuentes**, concluyen que a VOX lo trajo la **renta media-alta** (no los perdedores),
justifican la sección censal **por su homogeneidad interna**… **y no mencionan el MAUP ni una vez**.
Dos de los tres huecos los piden ellos mismos; el tercero es su omisión. **Pavía ya estaba en el
criterio de impacto por otros dos caminos independientes.**

**Fuentes de v2, ambas verificadas el 17-ago:** electoral, **Infoelectoral** (Mº Interior, desde 1976,
hasta mesa); socioeconómica, **INE — Atlas de Distribución de Renta de los Hogares (ADRH)**, operación
353, **hasta sección censal, 2015-2023**, con renta, Gini y P80/P20, y **cubriendo País Vasco y
Navarra** vía haciendas forales.

**Escalera de escalas (CORREGIDA):** `sección censal → distrito → municipio → provincia → CCAA`.
⚫ **La mesa queda fuera**: hay dato electoral pero **no hay socioeconómico** a ese nivel.
🔝 El frente vivo es **sección censal vs municipio** — no los mapas provinciales, que son de reparto
de escaños y ahí la provincia **es** la circunscripción legal.

🔴 **Riesgo que mata el diseño si se ignora:** el ADRH omite unidades de <100 habitantes → **la muestra
cambia con la escala**, y las que se caen son las diminutas del rural interior — donde el crecimiento de
VOX no es un residuo. **Obligatorio: fijar la muestra a las unidades presentes en todas las escalas y
reportar la selección por separado.** Es el mismo error que E0 ya cazó con las capitales.

🆕 **Fuente añadida el 17-ago, verificada: SERPAVI** (Mº Vivienda, precios del alquiler). Publica en
**los cinco mismos peldaños**, **2011-2023**, descarga libre, >2,5 M de alquileres/año. Da **dos
convocatorias más** que el Atlas y mide **el coste de vivir ahí**, no lo que se ingresa. ⚠️ Sin
comprobar si alguien lo ha cruzado con voto.

🔴 **Decisión sin tomar, y contamina la pregunta de escala:** ¿el voto se mide **sobre votos emitidos o
sobre censo**? La participación varía con el tamaño del municipio, así que elegir mal convierte un
efecto de participación en un falso efecto de escala. **Lo limpio: las dos.**

🟢 **Ensanche europeo, verificado y NO para ahora (§9 del alcance):** la política de cohesión reparte
fondos por umbral de PIB sobre **regiones NUTS2** (<75 % de la media = el grueso del dinero), y está
documentado que **Hungría, Polonia y Lituania separaron sus capitales** de sus NUTS2 ganando ventaja
en el reparto 2021-2027. **E0 ya topó con la huella** —las NUTS2 sin dato eran capitales, Varsovia y
Budapest entre ellas— sin saber qué estaba mirando. Consecuencia para el MVP: **escribirlo bilingüe
desde el principio** y meter una sección corta sobre el caso europeo, **sin ejecutarlo**.

📄 Alcance completo, antecedentes y quién actúa distinto: [`docs/v2_alcance.md`](v2_alcance.md).
🔴 **Y su §12 es la lista corta de lo que está SIN VERIFICAR** — seis cosas, con su coste al lado.
Ninguna bloquea construir; **todas bloquean publicar o presentar apoyándose en ellas.**

### 🔴 Por qué murió v1, en una línea, para no repetirlo
El diseño europeo anterior (EU-NED × ARDECO × PopuList/POPPA) se ejecutó en E0 y **no era viable**:
EU-NED no baja de NUTS2, el 22,9 % del voto español se quedaba sin veredicto de partido —justo los de
ámbito no estatal— y `partyfacts_id` no identifica al mismo partido entre fuentes. **Murieron las
fuentes, no la pregunta.** Cambiándolas, los tres motivos desaparecen por construcción.

### Estado de v2
- ✅ **Día 1** (`deaa81e`): `src/v2/descarga_infoelectoral.py` — reconocimiento de la fuente.
- ✅ **Día 2 — DESBLOQUEADO.** La descarga oficial funciona **con verificación TLS completa**
  (`src/v2/cadena_confianza.py` + `certs/`, 7 tests en verde). Bajados los tres ámbitos de 2019-11.
  🔴 **Y el diagnóstico anterior era falso:** `certifi` **sí** trae las raíces de la FNMT. Lo que
  pasa es que **el servidor del Ministerio manda la cadena incompleta** —omite la intermedia
  `AC Componentes Informáticos`— y OpenSSL, a diferencia del navegador, no la busca por AIA. La
  salida no fue *añadir una raíz* sino **completar una cadena cuyo ancla ya estaba avalada**:
  confianza nueva añadida, ninguna. Detalle en [§7-bis del alcance](v2_alcance.md).
- ✅ **Día 3 — el layout, LEÍDO desde código.** `src/v2/lector_doc.py` abre el `FICHEROS.doc` (OLE2
  de Word 97) **en Python puro** y `src/v2/layout_infoelectoral.py` lo convierte en un esquema con
  los **12 tipos de fichero**. Ninguna posición escrita a mano. **15 tests**, y el que cierra el
  asunto compara el esquema con los **diez `.dat` reales**: coinciden al byte.
  🔴 **Y la especificación miente en una frase:** dice `CR+LF` y los ficheros llevan **`LF` a
  secas**. Creerse esa frase desplaza un byte por línea y corrompe todos los campos a partir del
  segundo registro, con cifras que siguen pareciendo cifras. Ver §7-ter del alcance.
  ⚠️ **`antiword` está en esta máquina y NO se usa** — mismo motivo que el TLS: no está en Linux ni
  en CI.
- ✅ **Día 4 (19-ago) — mortalidad de secciones medida** (`src/v2/supervivencia_secciones.py`, 10
  tests). Ver el próximo paso, abajo. **33 tests en verde en total.**
- ✅ **Modo de trabajo nuevo, decidido el 19-ago:** este proyecto se hace **con G presente**, paso a
  paso, con pregunta de comprobación bloqueante en cada concepto, y **las mediciones se hacen CON él,
  no PARA él** (expectativa escrita antes de mirar, código enseñado antes de correr, número crudo
  antes de la interpretación). Las reglas están en `~/.claude/CLAUDE.md`. **No se baja la calidad; se
  baja el ritmo.**
- ✅ **Lenguaje: Python** (§5.6 del alcance). **Idioma: producto bilingüe ES/EN, conversación y docs
  internos en español** (§9.4).
- 🔴 **Y el peldaño "distrito" resultó no serlo:** 36.302 secciones · 10.485 distritos · **8.131
  municipios**, y solo el **13,4 %** de los municipios tiene más de un distrito. En el resto,
  distrito **es** municipio. O se declara, o el peldaño se retira (§7-ter-bis). **Sin decidir.**
- ✅ **`TOTA` ⊂ `MUNI` ⊂ `MESA`**, comprobado por SHA-256 entrada a entrada: el ámbito solo añade
  ficheros de resultados. **Con bajar `MESA` sobra.**
- ⏳ **Sin resolver:** quién actúa distinto porque esto exista (es el criterio flojo del proyecto).

---

## ⚫ Pipeline ESS — CONGELADO, no es la línea de trabajo

> El trabajo ESS/EFA **no está cancelado, está aparcado**: es infraestructura de medida para una capa
> que va **encima** de índices validados, y v2 no la necesita. **No lo retomes por inercia** — durante
> meses este fichero mandó "arreglar el EFA" y esa instrucción ya no es el próximo paso.

### Estado de scripts

| Script | Propósito | Estado |
|---|---|---|
| `R/ess_spain/spain_mcar_robust.R` | Test MCAR (Little + PKLM) | completado |
| `R/ess_spain/spain_mice_imputation.R` | Imputación mice PMM m=20 | completado |
| `R/ess_spain/spain_efa.R` | EFA pooled + test invarianza | pendiente |

> Rutas corregidas el 2026-08-12: `src/analysis/` nunca existió. El árbol canónico es
> `R/ess_spain/` y los scripts localizan los datos en `data/processed/ess/spain/` a partir
> de su propia ubicación. Ver `R/README.md`.

---

## Reglas críticas

- `data/raw/`: **SOLO LECTURA** — nunca modificar ni sobreescribir
- Antes de cualquier script R: invocar `@r-script-validator`
- Ante duda metodológica ESS: invocar `@methodology-guardian`
- Variables **fuera** del EFA: `lrscale`, `prtvt*`, `vote` (son validación, no features)
- `fa.pooled` recibe lista de **matrices de correlación**, no datasets
- `fa.parallel` con matrices requiere `n.obs` explícito

---

## ESTADO ACTUAL (2026-08-17)

**Línea viva: v2.** Ver arriba. `main` **sin pushear** (5 commits locales).

### Tests de v2 — y un aviso, porque el comando obvio falla

```
python -m pytest src/v2/ -q -m "not red"     # 6 en verde + 1 deseleccionado (necesita internet)
python -m pytest src/v2/ -q                  # los 7, con red
```

🔴 **Ojo: hay que correrlos con el Python DEL SISTEMA, no con `venv/`.** El venv del repo **no tiene
`pytest` instalado**, así que `./venv/Scripts/python.exe -m pytest` devuelve *"No module named pytest"* y
parece que no hay tests.

**Causa raíz, y no es que faltara instalarlo:** `requirements.txt` es un `pip freeze` completo y
**`pytest` no estaba declarado en él** pese a que el repo tiene suite de tests y los documenta.
✅ **Añadido el 17-ago.** Para dejar el venv en línea con el fichero:

```
./venv/Scripts/python.exe -m pip install -r requirements.txt
```

*(No se ejecutó desde la sesión: tocar el entorno de otro es suyo, no de quien audita.)*

**Código de v1 — histórico, no vivo.** `src/join_economico_electoral.py`,
`src/cobertura_partidos.py` y `src/ingestion/load_euned.py` produjeron los cuatro hallazgos de E0 y
**se conservan por su valor probatorio**, pero **no están en el camino de v2**. No construir encima
sin releer por qué murió v1.
🐛 Bug conocido y **no arreglado** en `src/ingestion/load_euned.py`: la regla `nativism>=7` **AND**
`far-right` ve solo el **10 % del voto** — *"no es conservadora: convierte 'no medido' en 'no
nacionalista'"*. Con v2 ese código deja de estar en el camino; **decidir si se arregla o se jubila**.

**ESS/EFA — congelado.** Sin cambios metodológicos: m=20, maxit=10, seed=42, PMM; ULS+oblimin,
`fa.pooled`, `mixedCor correct=0`, VARS_EXCLUIDAS; Little 2 bloques, JJ npar, PKLM 300/10/500 — todos
intactos y verificados. El EFA sigue con solución impropia (Heywood), 5 variables con comunalidad
<0.30 y MAP test pendientes. `data/raw/` sin tocar.

**Registro transversal:** `C:\Users\Guille\proyectos\REGISTRO.md`, enganchado a
`~/.claude/hooks/session_start.sh`, que avisa de lo vencido al arrancar.

---

## PRÓXIMO PASO EXACTO

⚫ ~~*Desbloquear la descarga de Infoelectoral*~~ — **hecho el 17-ago.** Ver el estado de v2 arriba.

⚫ ~~*Revisar el trabajo previo (SEA + dataset `renta`)*~~ — **hecho el 17-ago**, ver
[`docs/v2_trabajo_previo.md`](v2_trabajo_previo.md). **El hueco sigue abierto:** el SEA no cruza renta
con voto (solo padrón, una convocatoria) y sus mantenedores —Pavía y Pérez, que ya estaban en el
criterio de impacto— declaran por escrito que integrar la renta del INE sigue pendiente. El dataset
`renta` **se descarta**: sin año, 207 códigos con dos valores distintos, y falta Álava.

⚫ ~~*Transcribir el layout a un esquema*~~ — **hecho el 18-ago.** Ver el estado de v2 arriba.

⚫ ~~*Resolver la tensión de §12.7: ¿sobrevive una sección censal entre convocatorias?*~~ — **MEDIDO
el 19-ago con G. NO mata el diseño**, ver §6-bis del alcance. En resumen: de las 36.302 secciones de
nov-2019, **35.730 (98,42 %) siguen siendo el mismo sitio** en jul-2023. Rompen la comparación 572
(1,58 %): 268 muertas y **304 «particiones ocultas»** —conservan el código pero perdieron medio
cuerpo, y eran **invisibles** para el recuento obvio—. 🟢 Y el problema **vive solo en el peldaño más
fino**: las piezas de una partición no salen de su distrito, así que municipio, provincia y CCAA
están limpios. Plan decidido: **A reconstruir (solo si el emparejamiento es único) → C apartar y
declarar → B subir de peldaño, solo si fallan las dos**.
🆕 **Y salió un resultado publicable que no estaba en el plan:** nadie ha medido a qué ritmo se
reescribe la geografía electoral española más fina.

⚫ ~~*Comprobar si existe cartografía o tabla de correspondencias*~~ — **COMPROBADO el 19-ago, §6-ter
del alcance. Existen las dos.** Cartografía del INE `Secciones_2007`…`Secciones_2025`, libre, con
`CUSEC` que empalma directo con el fichero `09`. Y **`sc2sc`** en CRAN (v0.0.1-19, 2026-05-02, cubre
2001-2026): correspondencias **geométricas con proporciones de territorio**, no un simple
emparejamiento. **El plan A propio queda superado** y pasa a control cruzado.
🔴 **Y dos consecuencias que hay que tener presentes:** (a) `sc2sc` es de **Pérez y Pavía** — cuarto
camino independiente que lleva a la misma gente, lo que dice algo del campo; (b) es **R**, o sea el
primer uso de la válvula de escape de §5.6, abierta menos de una hora antes.
⚠️ **Y una afirmación de la mañana quedó degradada el mismo día:** *"nadie ha medido a qué ritmo se
reescribe la geografía electoral española"* pasa a **`[sin verificar si es novedoso]`**. Se escribió
antes de buscar quién lo había hecho. **Buscar primero, afirmar después.**

⚫ ~~*Escribir el preregistro antes de mirar los datos*~~ — ✅ **COMPLETO el 20/21-ago.** Ver abajo.

⚫ ~~*Leer la diana entera*~~ — **HECHO el 21-ago**, §2.2-bis del alcance. **El hueco del seccionado
sigue abierto:** alinean las secciones, citan sus métodos y **no publican ni una cifra**. Y cambió el
terreno de entrada: **no** por su párrafo de contexto (débil, rebatible en una línea) sino por **su
propio párrafo de limitaciones**, donde declaran que la validez depende de un supuesto que nadie ha
medido. 🔑 **La postura del proyecto, en una frase de G: *no les contradecimos, les completamos*.**

### ✅ EL PREREGISTRO, COMPLETO — ninguna decisión tomada después de ver un resultado

| | Decisión | §  |
|---|---|---|
| Objeto | **VOX por SIGLAS**, nunca por código (se reasignan cada elección) | 5.1 |
| Dependiente | **Cambio** del voto, descompuesto en **persuasión × movilización** | 5.1 |
| Explicativa | Renta como **nivel de partida**, del **año anterior** a la elección | 5.6-bis |
| Comparación | **nov-2019 → jul-2023** de titular · + pares consecutivos + base fija 2016 | 5.6-ter |
| Elecciones | **Solo generales** (5 en la ventana del Atlas) | 5.7 |
| Ámbito | **España**, con **Madrid como puente** de validación | 5.8 |
| Escalas | Cinco, **todas construidas desde abajo** | 6 |
| Muestra | Umbral de **100 residentes aplicado por nosotros**, todos los años | 5.2-bis |
| Pueblos <100 hab | **Fusionar** → marcar → descartar | 5.2-bis |
| Unidades | **Ponderadas por población** (+ sin ponderar) | 5.9 |
| Lenguaje / idioma | **Python** · producto bilingüe, conversación en español | 5.6 / 9.4 |

🔴 **Y el hallazgo que más cerca estuvo de arruinarlo todo (§5.2-bis):** desde los datos de 2020 el
Atlas **no deja huecos: los rellena**, asignando a las secciones pequeñas **el valor de su
municipio**. Eso pone **a cero por construcción** la variación intramunicipal — o sea, **fabrica el
resultado "la escala no importa"**, que es justo el que habíamos declarado publicable. Un hueco lo
ves; **un valor inventado te lo crees**.

## ▶️ PRÓXIMO PASO — ya no es decidir, es EJECUTAR

**(1) Bajar el Padrón por secciones censales** (2004-2022) **y el Censo Anual** (2021-2025) para tener
la población por sección. Es lo que permite aplicar el umbral de 100. ⚠️ El solape 2021-2022 **no es
un control de validez** —miden cosas distintas— sino la medida de **cuántas unidades quedan en la
frontera** según qué fuente (§12.15).

**(2) Bajar el ADRH y contar el agujero real:** cuántas secciones sin renta, cuánto censo suman,
cuántos votos a VOX hay dentro y dónde están. Eso **es** la capa de honestidad, no una nota al pie.

**(3) Cruzar.** Y solo entonces.

⚫ ~~*Retomar el EFA*~~ — era el próximo paso desde junio y **ya no lo es**. Ver el bloque congelado.

---

<!-- core_source_checkpoint: 2026-08-12_13-59 -->
