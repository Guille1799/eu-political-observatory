# EU Political Observatory — Skill para Cowork

## Descripción
Análisis de actitudes políticas y auge de partidos nacionalistas en 7 países de la UE usando datos ESS, EU-NED, POPPA y ARDECO. Usar para análisis de datos, pipeline EFA/CFA/IRT, consultas sobre variables ESS, partidos políticos, y desarrollo del dashboard.

## Contexto inicial (ejecutar SIEMPRE al arrancar)
```
eu_observatory:get_session_context(project="eu_observatory")
```
Para búsquedas específicas de variables ESS, partidos o datos electorales:
```
eu_observatory:search_context(query="[variable o concepto]", project="eu_observatory")
```

---

## SISTEMA DE ORQUESTACIÓN — Qué herramienta usar para cada tarea

| Tipo de tarea | Herramienta correcta |
|---|---|
| Análisis estadístico, interpretación, decisiones metodológicas | **Cowork / Claude Desktop** (aquí) |
| Escribir/editar scripts Python o R, verificar que corren | **Claude Code** |
| Exploración de datos en notebooks | **Cursor** o **Claude Code** |
| Buscar papers, estado del arte, metodología | Claude Desktop con Exa |
| Búsqueda y tracking de empleo | Cowork con skill job_hunter |

### Regla de oro
"Analiza estos datos y dime qué significa" → Cowork.
"Escribe este script y verifica que funciona" → Claude Code.

### Cómo arrancar Claude Code para este proyecto
```
1. Abrir pestaña Code en Claude Desktop
2. Seleccionar carpeta: C:\Users\Guille\proyectos\eu-political-observatory
3. Primera instrucción: "carga el contexto del proyecto y dime el estado actual"
```

---

## Limitaciones metodológicas conocidas (10) — revisar periódicamente
1. Correspondencia actitud-voto imperfecta
2. Escalas fallan cuando partido está en el poder
3. "Élite" significa cosas distintas
4. Sesgo de deseabilidad social
5. Invarianza temporal
6. Falacia ecológica
7. Endogeneidad
8. Pipeline ordinal→EFA→CFA→IRT
9. Sesgo clasificación partidos
10. Conflación ansiedad existencial vs. actitud

Ver `docs/EU_REFERENCIA.md` para detalle completo de cada una.

---

## Proyecto
- **Ruta:** `C:\Users\Guille\proyectos\eu-political-observatory\`
- **Referencia:** `docs/EU_REFERENCIA.md` — estado actual y decisiones
- **Onboarding:** `docs/onboarding.md` — setup, estructura, stack técnico
- **Checkpoints:** `C:\Users\Guille\proyectos\Contexto\eu-political-observatory\`

## Stack técnico
| Capa | Tecnología |
|---|---|
| Análisis | Python + R |
| ML/Stats | scikit-learn, lavaan, mirt |
| Datos | ESS, EU-NED, POPPA, PopuList 3.0, ARDECO, PartyFacts |
| Entorno | Python 3.13, venv en venv/ |

## Estructura de carpetas
```
data/raw/          — datos originales, NUNCA modificar
data/processed/    — datos limpios (incluye ess_variable_dictionary_classified.csv)
data/exports/      — outputs para dashboard
notebooks/ess/     — análisis ESS por país
src/               — scripts de ingestion, processing, analysis
docs/              — referencia, onboarding, handoffs
```

## Fuentes de datos indexadas en RAG
| Fuente | Contenido |
|---|---|
| ESS (7 rondas) | Actitudes ciudadanas, variables psicosociales |
| EU-NED | Resultados electorales por región NUTS 2 |
| POPPA | Scores populismo/nativismo por partido |
| PopuList 3.0 | Clasificación far-right/populist |
| ARDECO | PIB, desempleo, educación por NUTS 2 |
| PartyFacts/ParlGov | IDs cruzados de partidos |

## Comandos frecuentes
```powershell
# Activar entorno
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Git workflow
git add . && git commit -m "descripción" && git push
```

## Arquitectura de validación automática (hooks Claude Code)

Cadena de 4 niveles activa en Claude Code para scripts R y archivos de análisis:
- **Nivel 0:** bloquea data/raw/ sin LLM (instantáneo, siempre activo, exit 2)
- **Nivel 1:** qwen2.5-coder:1.5b — clasificador rápido (~1s, siempre en VRAM)
- **Nivel 2:** qwen3:8b — razonador metodológico con fallback a qwen:7b (~2-4s)
- **Nivel 3-4:** Haiku / methodology-guardian Sonnet (tokens, solo casos confirmados)

**Ollama debe estar corriendo** para que niveles 1-2 funcionen:
```powershell
ollama serve   # arrancar si no está activo
ollama ps      # verificar que está corriendo
```
Si Ollama está caído: niveles 1-2 se saltan, nivel 0 sigue activo. Nunca bloquea por error técnico.

Hook PreToolUse → cadena Ollama antes de cada edición en src/analysis/, notebooks/, .R
Hook Stop → check_efa_output.py si se tocó el pipeline EFA
Pre-commit hook → bloquea lrscale en EFA y writes en data/raw/ en cada git commit

**Subagents disponibles — invocar SOLO desde Claude Code:**
- `@methodology-guardian` — guardián metodológico activo (background:true)
- `@ess-variable-checker` — verifica recuperación RAG de variable específica
- `@r-script-validator` — valida script R antes de ejecutar

## Reglas
- Consultar RAG antes de inventar nombres de variables ESS
- No modificar data/raw/ nunca — el hook lo bloquea automáticamente
- Activar venv antes de cualquier comando Python
- Revisar las 10 limitaciones metodológicas al inicio de cada análisis nuevo
- Para código → Claude Code, no Cowork
- Ollama corriendo para validación completa: `ollama serve`
- Invocar @r-script-validator antes de ejecutar cualquier script R nuevo o modificado
