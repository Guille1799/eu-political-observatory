---
paths: **/*.R
alwaysApply: false
---

# Reglas metodológicas ESS — carga solo en archivos R

## Variables prohibidas en EFA (siempre)
NUNCA incluir en fa(), fa.parallel(), o cualquier EFA: lrscale, prtvt*, vote, cualquier variable de outcome político o escala Likert de actitud política.

## Funciones críticas — checks obligatorios

- **mixedCor():** DEBE especificar p=, d=, c= EXPLÍCITAMENTE (bug auto-detección NO CORREGIDO en psych 2.6.x — doc oficial avisa). NUNCA confiar en auto-detección.
- **fa.parallel():** SIEMPRE con `n.obs=nrow(data)` explícito si se pasa matriz de correlación. fa.parallel.poly está DEPRECATED — usar fa.parallel(cor="poly").
- **fa.pooled():** recibe MATRICES de correlación, NO datasets. Verificar tipo antes de pasar argumento.
- **fa() en psych 2.6.5+:** SIEMPRE especificar `n.rotations=` explícitamente. Default cambió a 20 (antes=1) — puede cambiar resultados sin aviso. Usar `n.rotations=1` para reproducir resultados previos a 2.6.5.
- **psych fa() chi-square:** bug corregido en 2.6.1 — versiones <2.6.1 calculaban el doble del valor correcto. Comparaciones con output histórico de psych <2.6.1 requieren re-cálculo.
- **mice():** imputación en datos completos antes de EFA. Nunca EFA sobre datos imputados directamente.

## ELIMINADO en semTools 0.5-8 (feb 2026) — BLOQUEAR si se detectan:
- semTools::measurementInvariance() → ELIMINADA. Migrar a lavTestScore() + modelos anidados
- semTools::measurementInvarianceCat() → ELIMINADA. Igual migración.
- semTools::longInvariance() → ELIMINADA. Igual migración.
- semTools::runMI() → ELIMINADA. Migrar a **lavaan.mi** (CRAN mar 2025).

## lavaan.mi — sintaxis DIFERENTE a semTools::runMI:
- `library(lavaan.mi)` SIEMPRE explícito (no lazy-load).
- NO existe argumento `fun=`. Usar: `cfa.mi(model, data=imp_mids, ordered=nombres_items, estimator="WLSMV", group="cntry", omit.imps=c("no.conv","no.se"))`
- `lavTestLRT.mi()`: argumento `test=` renombrado a `pool.method=`. **Para WLSMV: SOLO `pool.method="D2"` es válido.**
- Secuencia invarianza ordinal WLSMV: **configural → thresholds → thresholds+loadings** (NO loadings antes de thresholds).
- `cfi.robust`/`rmsea.robust` pueden devolver NA con WLSMV — reportar `.scaled` como equivalente a Mplus.
- Requiere lavaan >= 0.6-20.

## lavaan 0.6-20 — cambio CRÍTICO para datos ordinales ESS (WLSMV):
Secuencia correcta para invarianza: **configural → thresholds → thresholds+loadings** (NO loadings directamente después de configural).

## EGAnet 2.4.1 — cambios de nombre que rompen código:
- `network.nonconvex` RENOMBRADO a `network.regularization` (dentro del propio EGAnet).
- `net.loads()` default cambió a `loading.method = "revised"`. Usar `loading.method = "original"` para reproducir resultados anteriores a v2.0.6.
- `EGM` y `EGM.compare` eliminados en v2.4.0 — NO restaurados en 2.4.1. No usar ni mencionar.
- `bootEGA(type="parametric")`: genera datasets de distribución NORMAL multivariada (NO ordinal). Para datos ESS Likert/ordinal: SIEMPRE usar `type="resampling"`.
- `itemDiagnostics()` nueva (v2.3.0): detecta dependencia local, outliers — recomendable antes de confirmar estructura.

## MCAR tests — actualización:
- `MCARtest::little_test(X, type = "mean&cov")`: PREFERIDO para ESS con muchas variables.
- **BREAKING CHANGE MCARtest 1.3 (CRAN 2025-06-26):** parámetro `alpha=` ELIMINADO. La función devuelve el p-value directamente (no un Boolean). Migrar a: `resultado <- little_test(X, type="mean&cov"); if (resultado$p.value < 0.05) { ... }`.
- `naniar::mcar_test()` y `misty::na.test()`: limitados a ~30 variables fiables.

## Checks adicionales metodológicos:
- fa.parallel sugiere N factores: contrastar con EGAnet::EGA() — supera fa.parallel en +16.5pp accuracy (71% vs 54.5%).
- Invarianza métrica falla en >2 grupos cross-nacionales: proponer Penalized Alignment (Asparouhov & Muthén 2023). Sin implementación R pública — solo Mplus 8.10+. `sirt::invariance.alignment()` implementa alignment CLÁSICO 2014 (diferente).

## data/raw/ — READ ONLY ABSOLUTO
Jamás escribir, modificar, o eliminar nada en data/raw/. Si necesitas modificar: copia a data/processed/ primero.

## Antes de ejecutar cualquier script R
Invocar @r-script-validator. No ejecutar sin validación previa.
