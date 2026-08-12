# EU Political Observatory — Referencia Metodológica Completa

> Cargado automáticamente por `get_session_context(project="eu_observatory")`.
> Contiene metodología ESS completa + estado del proyecto.

---

## Flujo metodológico ESS completo

1. **Selección variables EFA** — exclusiones documentadas con razón por grupo (técnicas, household, comportamiento, nominales, controles)
2. **Test MCAR** (R: `spain_mcar_robust.R`) — Little + Jamshidian/Jalal + PKLM. Resultado: MAR, valida imputación múltiple.
3. **Imputación múltiple** (R: `spain_mice_imputation.R`) — mice PMM m=20. Genera 20 datasets + pooled (modo).
4. **KDE plots validación** — comparar distribuciones reales vs imputadas.
5. **EFA por país** — `fa.pooled` sobre 20 datasets; `mixedCor` (psych): policóricas para vars ≤8 cats, Pearson para vars 0-10.
6. **Test invarianza** — configural / métrica / escalar (MG-CFA). Fischer (2025) como referencia.
7. **Índice comparativo** — factores invariantes + índices por país.
8. **Validación** — `lrscale` (principal), `prtvt*` (secundaria, según disponibilidad por país/ronda).
9. **CFA + IRT** — cuando estructura confirmada. IRT para escalas cross-nacional (Van Hauwaert et al. 2019).

---

## 10 Fallos metodológicos identificados

| # | Fallo | Corrección implementada |
|---|-------|------------------------|
| 1 | Correspondencia imperfecta actitudes-voto | No afirmar causalidad; validar con lrscale, no prtvt* |
| 2 | Escalas fallan cuando partido está en el poder (HU, PL) | EFA por país; añadir trstun y trstep |
| 3 | "Élite" significa distinto por país | EFA por país |
| 4 | Sesgo deseabilidad social | lrscale en vez de prtvt*; documentar subestimación primeros años |
| 5 | Invarianza temporal (desconfianza 2008 ≠ 2022) | Test invarianza temporal dentro de cada país |
| 6 | Falacia ecológica al agregar ESS a NUTS2 | Modelos multinivel; Gnaldi et al. 2015 |
| 7 | Endogeneidad actitudes-voto | Documentar como correlación, no causalidad |
| 8 | Variables ordinales vs EFA | Flujo EFA → CFA → IRT (Van Hauwaert et al. 2019) |
| 9 | Sesgo clasificación partidos | Doble validación POPPA + PopuList implementada |
| 10 | Ansiedad existencial vs actitud política | Documentar explícitamente qué mide el índice en el dashboard |

---

## Variables de control — validadas por literatura

| Variable | Descripción | Referencia |
|----------|-------------|------------|
| agea | Edad | Arzheimer 2009, Polacko 2022 |
| gndr | Género | Estándar universal |
| eduyrs / eisced | Educación | Estándar universal |
| domicil | Rural/urbano | Dilger 2026, Polacko 2022 |
| uemp5yr / uemp3m | Desempleo reciente (objetivo) | Arzheimer 2009, Guiso 2024 |
| hinctnta | Ingresos totales hogar | Dilger 2026 |
| rlgdgr | Religiosidad | Dilger 2026 — CONTROL, no entra en EFA |
| crmvct | Victimización real | Control para aesfdrk |

## Variables de validación — NO entran en el índice

| Variable | Razón |
|----------|-------|
| lrscale | Validación principal — circularidad si entra en EFA |
| vote | Si votó en última elección |
| prtvt* | Partido votado: DE (R7-9), FR (R6-8), PL (R8-9), HU (R7-8), ES (R10-11) |

---

## Metodología de clasificación de partidos nacionalistas

- **Umbral**: `nativism >= 7.0` en POPPA **Y** `far-right` en PopuList 3.0 (ambas condiciones).
- **Un solo sitio** (2026-08-11): el valor vive en `src/ingestion/parameters.py`
  (`NATIVISM_THRESHOLD`), con su procedencia al lado. `load_euned.py` y `load_parlgov.py`
  lo importan como valor por defecto — ya no lo redeclaran. Antes estaba duplicado como
  literal `7.0` en los dos scripts.
- **Procedencia del 7.0**: convención del proyecto, decidida en la sesión de diseño del
  2026-05-05 con la justificación "un score de 7+ se considera alto" — **sin cita**. No hay
  en el repo ninguna referencia (autor/año) que fije 7.0 como umbral canónico de POPPA. Su
  mitigación declarada es la doble condición con PopuList, adoptada precisamente para no
  depender de un corte numérico arbitrario. Nunca se ha corrido análisis de sensibilidad.
- **Índice ponderado**: `nationalist_weighted_index = sum(vote_share * nativism) / 10`
- **Futuro**: sustituir threshold fijo por análisis factorial sobre POPPA; validar con Vox, AfD, RN, FdI, Fidesz, SD.

---

## Literatura clave

| Referencia | Relevancia |
|-----------|-----------|
| Inglehart & Norris (2016) | EFA Varimax sobre ESS — referencia metodológica principal |
| Guiso et al. (2024) | hincfel como proxy inseguridad económica individual |
| Dolci & Melli (2025) | PopuList + ParlGov + flujo EFA → regresión logística |
| Van Hauwaert et al. (2019) | IRT para escalas populistas cross-nacional (Fallo 8) |
| Fischer (2025) | Invarianza Schwartz en ESS 11 rondas con MG-CFA |
| Falkner et al. (2024) | Escalas populistas fallan cuando partido en el poder (Fallo 2) |
| Dilger (2026) | Variables de control estándar |
| Gnaldi et al. (2015) | Falacia ecológica y modelos multinivel (Fallo 6) |
| Arzheimer (2009) | agea, uemp* como predictores |
| Polacko (2022) | agea, domicil |
| Nickel et al. (2024) | imsmetn — invarianza cross-cultural débil (excluida de EFA) |

---

## Arquitectura y datos

- **Flujo**: `data/raw/` → `src/ingestion/` → PostgreSQL → `src/api/` FastAPI → dashboard Next.js
- `data/raw/`: originales, nunca modificar, nunca subir a GitHub
- `data/processed/`: intermedios limpios, no subir
- `data/exports/`: outputs para dashboard, sí se pueden subir

### Fuentes implementadas
ARDECO, EU-NED, POPPA v2, PopuList 3.0, ParlGov 2024, crosswalk PartyFacts-ParlGov, ESS (en proceso)

### Fuentes pendientes
Eurobarometer, Manifesto Project, elecciones España 2023, paneles longitudinales (POLAT, SOEP, ELIPSS)

### PostgreSQL (tabla relevantes)
`ardeco_unemployment`, `ardeco_gdp`, `ardeco_education`, `nationalist_vote`, `nationalist_vote_national`

---

## Notas técnicas de R

- `fa.parallel` con matrices de correlación requiere `n.obs` explícito
- `fa.pooled` recibe lista de matrices de correlación (no lista de datasets)
- PKLM con nrep=500 tarda ~2h en Windows con 21k filas. Para otros países: nrep=200
- `naniar::mcar_test()` tiene límite ~30 variables con prelim.norm — usar `misty` en su lugar para n>30 vars
- `mixedCor` de psych: policóricas solo para vars ≤8 categorías; Pearson para vars 0-10
- Los 20 datasets imputados (spain_core_imputed_m01.csv…m20.csv) NO tienen las 5 vars excluidas en pre-EFA — la exclusión se hace en el script R al cargar

---

## Limitaciones documentadas

- Cobertura NUTS2 irregular entre países
- EU-NED hasta 2020
- España regional desde 2019, Alemania 2013/2017
- Hungría: cambio histórico Fidesz requiere manejo especial
- ESS sin NUTS2 (inferir por domicil es aproximación)
- Italia: solo 6 rondas ESS (umbral 8+ no alcanzado) — decisión pendiente sobre tratamiento

---

## ESTADO ACTUAL

Proyecto pausado desde 2026-06. Pipeline ESS España: MCAR test completado (MAR confirmado), imputación múltiple mice PMM m=20 lista, 20 datasets generados.
EFA pooled sobre matrices pendiente. Clasificación de partidos implementada (POPPA + PopuList).

## PRÓXIMO PASO EXACTO

Retomar pipeline ESS España: ejecutar `spain_efa.R` con `fa.pooled` sobre 20 matrices imputadas → test invarianza configural/métrica/escalar → índice comparativo por país.
