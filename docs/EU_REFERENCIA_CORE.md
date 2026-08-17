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
- ✅ **La especificación del layout viaja DENTRO del zip** (`FICHEROS.doc`). No hay que suponerlo ni
  buscarlo fuera. **Pendiente: transcribirla a un esquema.**
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

**(1) Transcribir el layout a un esquema** desde el `FICHEROS.doc` que ya está extraído en
`data/external/infoelectoral/especificacion/`. Es un binario OLE2 (Word 97) — hay que sacarle el
texto. **Se lee, no se supone.** 🟢 Y ahora hay con qué contrastarlo: los lectores `read03`…`read12`
del paquete `infoelectoral` son una transcripción independiente del mismo layout.

**(2) Escribir, ANTES de mirar los datos**, la regla de qué candidaturas cuentan como VOX cuando
concurre en coalición · la elección de **denominador** (votos emitidos y/o censo) **y** la regla de
muestra fija entre escalas. El preregistro entra en el MVP.

⚫ ~~*Retomar el EFA*~~ — era el próximo paso desde junio y **ya no lo es**. Ver el bloque congelado.

---

<!-- core_source_checkpoint: 2026-08-12_13-59 -->
