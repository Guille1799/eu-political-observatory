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
#   - Regla del diseño europeo (v1): `nativism >= 7.0` en POPPA Y far-right en
#     PopuList 3.0. Las dos condiciones, de dos fuentes independientes.
#   - Origen del 7.0: decidido en la sesión de diseño del 2026-05-05, con la
#     justificación "un score de 7+ en nativismo se considera alto".
#   - HONESTIDAD: esa justificación NO trae cita. No hay en el repo ninguna referencia
#     concreta (autor/año) que fije 7.0 como umbral canónico de POPPA. El corte es una
#     convención del proyecto, no un valor tomado de la literatura. Lo que sí está
#     documentado es su mitigación: la doble condición con PopuList, adoptada
#     precisamente para no depender de un umbral numérico arbitrario.
#   - PENDIENTE que quedó sin hacer: sustituir el umbral fijo por análisis factorial
#     sobre POPPA, y validar contra Vox, AfD, RN, FdI, Fidesz y SD.
#   - Sensibilidad: nunca se ha corrido. El rango contemplado en el diseño era 6.0-8.0.
#
# ⚫ Este umbral pertenece al diseño europeo (v1), que se RETIRÓ tras ejecutarse: entre
# otras cosas, porque clasificar partidos por etiqueta ideológica resultó no ser fiable
# entre fuentes. La línea actual no usa este parámetro — define su objeto por dónde
# concurre un partido, no por cómo lo etiqueta un experto. Ver `docs/decisiones/`.
NATIVISM_THRESHOLD = 7.0
