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

Pipeline ESS España sin cambios metodológicos: m=20, maxit=10, seed=42, PMM; ULS+oblimin,
`fa.pooled`, `mixedCor correct=0`, VARS_EXCLUIDAS; Little 2 bloques, JJ npar, PKLM 300/10/500 —
todos intactos y verificados. `data/raw/` sin tocar.

El EFA sigue donde estaba: primera iteración con solución impropia (Heywood), 5 variables con
comunalidad <0.30 pendientes, MAP test pendiente. **Nada de esta sesión avanzó el análisis** —
fue toda infraestructura e higiene.

`main` en `d78529e`, empujado. Ramas `claude/*` borradas (fusionadas). Working tree limpio.
Tres worktrees reducidos a uno.

**Artefacto nuevo y transversal: `C:\Users\Guille\proyectos\REGISTRO.md`.** Nueve entradas.
Cinco campos por entrada (disparador, señal de uso medible, quién lo hace cumplir, caducidad,
estado) y una regla: llegada la fecha, o hay señal de uso, o la cosa se quita. Enganchado a
`~/.claude/hooks/session_start.sh`, que avisa de lo vencido al arrancar sesión.

---

## PRÓXIMO PASO EXACTO

Retomar el análisis, que lleva parado desde mayo: **verificar/arreglar la solución EFA** —
número de factores (paralelo/MAP, no 12), tratar los Heywood, validar con
`@methodology-guardian` — antes de tocar nada más. Ejecutar con
`Rscript R/ess_spain/spain_efa.R` (ruta nueva).

Antes de eso, las entradas del registro que vencen: **19 ago** (duplicado
`autohealth-monitor.py`, fósiles de log) y **26 ago** (`pipeline-coordinator`, invariante C5).

---

<!-- core_source_checkpoint: 2026-08-12_13-59 -->
