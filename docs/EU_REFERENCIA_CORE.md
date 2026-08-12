# EU_REFERENCIA_CORE — eu-political-observatory
> Cargado automáticamente por `get_session_context(project="eu_observatory")`.
> Metodología ESS completa: `docs/EU_REFERENCIA.md`.
> Última actualización: 2026-06-11

---

## Pipeline ESS — Estado de scripts

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

## ESTADO ACTUAL

Proyecto pausado desde 2026-06. MCAR completado (MAR confirmado). Imputación múltiple m=20 completada — 20 datasets generados en `data/processed/`.
EFA pooled sobre matrices pendiente de ejecutar / revisar.

> 🔴 **AVISO — la solución EFA guardada parece IMPROPIA (detectado 2026-07-21 por el fan-out de perfil de JobHunter,
> pendiente de tu verificación).** `spain_efa.R:60,86-160` produce una solución con **12 factores, comunalidades ≈0.995
> (casos HEYWOOD) y ~58% de varianza** — señales clásicas de **sobre-extracción / solución no admisible**. Si es así,
> NO se puede construir nada encima (índice, capa de legibilidad) sin arreglarlo primero: sería cimentar sobre arena.
> **Antes de dar por bueno el EFA:** revisar nº de factores (paralelo/MAP, no 12), tratar los Heywood, y validar con
> `@methodology-guardian`. NB metodológica adicional del fan-out: el "pooling" de la imputación usa la **MODA**, no las
> **reglas de Rubin** — revisar si aplica. *(Estos hallazgos son de subagentes leyendo el repo; confírmalos tú.)*
>
> ✅ Higiene (RESUELTO el 2026-08-12): los `.R` estaban duplicados en `R/ess_spain/` (versionado) y en
> `data/processed/ess/spain/` (gitignoreado), y los versionados instruían ejecutar la copia invisible.
> `R/ess_spain/` es ya el árbol canónico, las copias fantasma están borradas, `R/README.md` escrito, y los
> scripts derivan la ruta de datos de su propia ubicación en vez de asumir el directorio de trabajo.

## PRÓXIMO PASO EXACTO

Retomar pipeline: **(1) VERIFICAR/ARREGLAR la solución EFA** (ver aviso arriba — nº de factores, Heywood) antes de nada;
luego `fa.pooled` limpio sobre 20 matrices → test invarianza configural/métrica/escalar → índice comparativo por país.
