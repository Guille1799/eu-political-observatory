# EU_REFERENCIA_CORE — eu-political-observatory
> Cargado automáticamente por `get_session_context(project="eu_observatory")`.
> Metodología ESS completa: `docs/EU_REFERENCIA.md`.
> **Última actualización: 2026-08-17.**

---

## 🔝 LO PRIMERO: qué es este proyecto AHORA (v2, decidido el 2026-08-16)

**Pregunta:** ¿dónde y por qué crece el voto a **partidos de ámbito no estatal (PANE)** en España — y
**cambia la respuesta según la escala territorial a la que mires**?

Esa segunda mitad **es el producto**, no un chequeo: el mismo dato puede contar una historia agregado
por municipios y otra por provincias (*modifiable areal unit problem*). Junto a ella va la **capa de
honestidad**: un mapa que **se niega a pintar** donde no hay base y lo dice.

**Fuentes de v2, ambas verificadas el 17-ago:** electoral, **Infoelectoral** (Mº Interior, desde 1976,
hasta mesa); socioeconómica, **INE — Atlas de Distribución de Renta de los Hogares (ADRH)**, operación
353, **hasta sección censal, 2015-2023**, con renta, Gini y P80/P20, y **cubriendo País Vasco y
Navarra** vía haciendas forales.

**Escalera de escalas (CORREGIDA):** `sección censal → distrito → municipio → provincia → CCAA`.
⚫ **La mesa queda fuera**: hay dato electoral pero **no hay socioeconómico** a ese nivel.
🔝 El frente vivo es **sección censal vs municipio** — no los mapas provinciales, que son de reparto
de escaños y ahí la provincia **es** la circunscripción legal.

🔴 **Riesgo que mata el diseño si se ignora:** el ADRH omite unidades de <100 habitantes → **la muestra
cambia con la escala**, y el sesgo apunta a los municipios diminutos del rural interior, que es donde
vive el voto PANE. **Obligatorio: fijar la muestra a las unidades presentes en todas las escalas y
reportar la selección por separado.** Es el mismo error que E0 ya cazó con las capitales.

📄 Alcance completo, antecedentes y quién actúa distinto: [`docs/v2_alcance.md`](v2_alcance.md).

### 🔴 Por qué murió v1, en una línea, para no repetirlo
El diseño europeo anterior (EU-NED × ARDECO × PopuList/POPPA) se ejecutó en E0 y **no era viable**:
EU-NED no baja de NUTS2, el 22,9 % del voto español se quedaba sin veredicto de partido —justo los de
ámbito no estatal— y `partyfacts_id` no identifica al mismo partido entre fuentes. **Murieron las
fuentes, no la pregunta.** Cambiándolas, los tres motivos desaparecen por construcción.

### Estado de v2
- ✅ **Día 1 hecho** (`deaa81e`): `src/v2/descarga_infoelectoral.py` — reconocimiento de la fuente.
- 🔴 **Bloqueo activo:** el certificado de `infoelectoral.interior.gob.es` es auténtico pero lo emite
  la **FNMT-RCM**, que no está en el almacén de raíces de Mozilla → ni en Python ni en `certifi`.
  **La fuente oficial no se baja desde código sin añadir esa raíz.** Se dejó fallando a propósito:
  **no desactivar la verificación TLS** — eso invalidaría la procedencia, que es medio proyecto.
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

**Línea viva: v2.** Ver arriba. `main` en `deaa81e`, **sin pushear**. Working tree limpio.

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

**Desbloquear la descarga de Infoelectoral**: obtener la raíz de la **FNMT-RCM** por un canal
verificable, añadirla a un bundle propio del repo, y volver a correr
`python src/v2/descarga_infoelectoral.py`. Hasta que eso funcione **no se ha comprobado el patrón de
nombre de fichero** y no se da por bueno.

🟢 **Atajo verificado:** los paquetes de R `infoelectoral` (Héctor Meleiro) y `pollspain` (Javier
Álvarez-Liébana) **ya descargan de Infoelectoral** → han resuelto lo de la FNMT. Mirar cómo lo hacen
antes que buscar la raíz a ciegas.

Después, en este orden: (1) **revisar el SEA (Spanish Electoral Archive, Harvard Dataverse)** y el
dataset `renta` del paquete `infoelectoral` (>34.000 filas ya cruzando renta INE × sección censal) —
**antes de escribir una línea de fontanería**: puede ahorrar semanas o mostrar que parte ya está
hecha; (2) leer la especificación oficial de los ficheros de ancho fijo — **no suponer el layout**;
(3) escribir **antes de mirar los datos** el umbral operativo que define PANE **y** la regla de
muestra fija entre escalas.

⚫ ~~*Retomar el EFA*~~ — era el próximo paso desde junio y **ya no lo es**. Ver el bloque congelado.

---

<!-- core_source_checkpoint: 2026-08-12_13-59 -->
