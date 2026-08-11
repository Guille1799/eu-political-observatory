"""Parámetros metodológicos compartidos por los scripts de ingesta.

Un corte metodológico vive en UN solo sitio y lleva su procedencia al lado. Si el valor
cambia, cambia aquí y en ninguna otra parte: los scripts lo importan, no lo redeclaran.
"""

# ── NATIVISM_THRESHOLD ───────────────────────────────────────────────────────
# Score mínimo de nativismo (POPPA, escala 0-10) para que un partido sea candidato a
# "nacionalista". NO basta por sí solo: la clasificación exige ADEMÁS que PopuList 3.0
# marque al partido como far-right (doble condición de dos fuentes independientes).
# Usado por: load_euned.calculate_nationalist_vote y
#            load_parlgov.calculate_nationalist_vote_parlgov.
#
# PROCEDENCIA (verificada 2026-08-11, no inferida):
#   - Regla declarada en `docs/EU_REFERENCIA.md` → "Metodología de clasificación de
#     partidos nacionalistas": `nativism >= 7.0` en POPPA Y far-right en PopuList 3.0.
#   - Origen del 7.0: decidido en la sesión de diseño del 2026-05-05
#     (`docs/claude-conversations/2026-05-05-claude.md`, ~línea 6632) con la
#     justificación "un score de 7+ en nativismo se considera alto".
#   - HONESTIDAD: esa justificación NO trae cita. No hay en el repo ninguna referencia
#     concreta (autor/año) que fije 7.0 como umbral canónico de POPPA. El corte es una
#     convención del proyecto, no un valor tomado de la literatura. Lo que sí está
#     documentado es su mitigación: la doble condición con PopuList, adoptada
#     precisamente para no depender de un umbral numérico arbitrario.
#   - PENDIENTE (ya registrado en `docs/EU_REFERENCIA.md`): sustituir el umbral fijo por
#     análisis factorial sobre POPPA, y validar contra Vox, AfD, RN, FdI, Fidesz y SD.
#   - Sensibilidad: nunca se ha corrido. El rango contemplado en el diseño era 6.0-8.0.
#
# Candidato del registro `capa-normativa` / `capa-normativa`. Todavía NO migrado: el paso
# de ahora es un solo sitio; la migración al registro es una tarea aparte.
NATIVISM_THRESHOLD = 7.0
