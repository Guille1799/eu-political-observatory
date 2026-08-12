# eu_observatory — Skill para Claude Code

## Descripción
Análisis de actitudes políticas y partidos nacionalistas en 7 países UE. Esta skill es para trabajo de DESARROLLO: escribir scripts, editar código Python/R, verificar que corren correctamente.

## Contexto inicial (ejecutar SIEMPRE al arrancar)
```
eu_observatory:get_session_context(project="eu_observatory")
```

---

## ROL DE CLAUDE CODE EN ESTE PROYECTO

Claude Code hace el trabajo de código. Cowork/Claude Desktop hace análisis y decisiones.

Cuando Cowork delega una tarea a Claude Code, llega como instrucción concreta:
"Escribe un script que haga X y verifica que corre sin errores."

Flujo estándar:
1. get_session_context para cargar estado
2. search_context si necesitas contexto de variables ESS o metodología
3. Escribir o editar el script
4. Ejecutar y verificar output
5. Reportar resultado

Si surge una decisión metodológica no trivial → pausar y consultar con Cowork/Claude Desktop.

---

## Restricciones de entorno

### bash_tool no llega a rutas Windows
Usar siempre: filesystem:read_text_file, filesystem:edit_file, filesystem:write_file
No usar bash_tool para archivos de C:\Users\Guille\...

### Entorno Python
Siempre activar venv antes de ejecutar scripts:
```powershell
C:\Users\Guille\proyectos\eu-political-observatory\venv\Scripts\activate
```

### Datos raw — protegidos
Nunca modificar nada en `data/raw/`. Solo lectura.

---

## Estructura del proyecto
```
data/raw/          — datos originales (READ ONLY)
data/processed/    — datos limpios, ess_variable_dictionary_classified.csv
data/exports/      — outputs para dashboard
notebooks/ess/     — análisis por país
src/ingestion/     — descarga de datos
src/processing/    — limpieza y transformación
src/analysis/      — modelos, correlaciones
docs/              — EU_REFERENCIA_CORE.md (get_session_context), EU_REFERENCIA.md (metodología completa), onboarding.md
```

## Variables ESS — cómo encontrarlas
Antes de inventar nombres de variables, consultar el RAG:
```
eu_observatory:search_context(query="nombre concepto en español", project="eu_observatory")
```
El diccionario `ess_variable_dictionary_classified.csv` está indexado con label_es (español).

## Fuentes de datos indexadas
| Fuente | Archivo clave |
|---|---|
| ESS | ess_variable_dictionary_classified.csv |
| Partidos | poppa_integrated_v2.csv, view_party.csv |
| Elecciones | partyfacts-parlgov-ids.csv |
| Regional | ARDECO (excluido del RAG por tamaño) |

## Comandos frecuentes
```powershell
# Activar entorno
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar script
python src/analysis/nombre_script.py

# Git
git add . && git commit -m "descripción" && git push
```

## Rutas críticas
- Raíz: `C:\Users\Guille\proyectos\eu-political-observatory\`
- Referencia CORE: `docs/EU_REFERENCIA_CORE.md` (cargada por get_session_context)
- Referencia completa: `docs/EU_REFERENCIA.md` (metodología ESS, leer bajo demanda)
- Checkpoints: `C:\Users\Guille\proyectos\Contexto\eu-political-observatory\`
