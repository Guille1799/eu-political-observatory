# EU Political Observatory — Onboarding Guide

## ¿Qué es este proyecto? *(act. 2026-08-17)*

**Pipelines reproducibles y con procedencia para estudiar política territorial**, montados para que cada
número se pueda rastrear hasta su fuente y para que **las decisiones de medida se vean en vez de darse
por supuestas**.

**La línea de trabajo actual (v2) es española y subnacional:** *¿dónde y por qué crece el voto a partidos
de ámbito no estatal (PANE), y cambia la respuesta según la escala territorial a la que se mire?*
**La segunda mitad es el producto.** 📄 Alcance completo: [`v2_alcance.md`](v2_alcance.md).

> ⚫ **Esta página decía antes:** *"un dashboard educativo e interactivo… de partidos nacionalistas en 7
> países de la UE"*. **Las tres cosas han dejado de ser ciertas** y se corrigen aquí en vez de en un
> índice aparte:
> - **No hay dashboard**, y es deliberado: un panel donde se cruzan decenas de variables a voluntad es
>   una máquina de correlaciones espurias. Ver §9 del alcance, *"qué NO hace este proyecto"*.
> - **No son 7 países**: el diseño europeo se ejecutó y no era viable con sus fuentes. Ahora es España,
>   que a cambio da escalas mucho más finas.
> - **No es "partidos nacionalistas"**: esa etiqueta es un juicio ideológico y estaba mal codificada en
>   las fuentes. El objeto se define por **dónde concurre** un partido.

---

## Conceptos fundamentales

### ¿Qué es Git?
Sistema de control de versiones que registra todos los cambios en el código. Funciona como un álbum de fotos de tu proyecto.
- `git add .` — selecciona los archivos para la foto
- `git commit -m "mensaje"` — hace la foto con un mensaje descriptivo
- `git push` — sube las fotos a GitHub (la nube)
- `git init` — inicializa Git en una carpeta nueva

### ¿Qué es un entorno virtual (venv)?
Una burbuja aislada de Python específica para este proyecto. Las librerías instaladas aquí no afectan a otros proyectos ni al Python global.
- Crear: `py -3.13 -m venv venv`
- Activar (Git Bash): `source venv/Scripts/activate`
- Activar (PowerShell): `venv\Scripts\activate`
- Desactivar: `deactivate`
- IMPORTANTE: siempre debe estar activo (verás `(venv)`) antes de cualquier comando Python

### ¿Qué es una librería?
Código extra que alguien ya escribió para hacer tareas complejas. Se instalan con pip.
- Instalar todas: `pip install -r requirements.txt`
- Guardar versiones exactas: `pip freeze > requirements.txt`

### ¿Qué es un wheel?
Paquete precompilado de una librería — listo para instalar sin necesitar herramientas de compilación. Si una librería no tiene wheel para tu versión de Python, pip intenta compilarla desde fuente y puede fallar.

### ¿Qué es el .gitignore?
Archivo que le dice a Git qué carpetas y archivos ignorar. En este proyecto ignoramos:
- `venv/` — la burbuja es personal, cada uno crea la suya
- `data/raw/` y `data/processed/` — demasiado pesados para GitHub
- `.cursor/` y `.vscode/` — configuración personal del editor

### ¿Qué es el .cursorrules?
Archivo que Cursor lee automáticamente en cada sesión. Contiene instrucciones sobre el proyecto, el stack técnico, y cómo trabajar con Guille. Si Cursor pierde el contexto, abrir una conversación nueva — releerá el archivo.

---

## Setup del proyecto paso a paso

### Primera vez
```bash
# 1. Clonar el repositorio
git clone https://github.com/Guille1799/eu-political-observatory.git
cd eu-political-observatory

# 2. Crear entorno virtual con Python 3.13
py -3.13 -m venv venv

# 3. Activar entorno virtual
source venv/Scripts/activate  # Git Bash
# o
venv\Scripts\activate  # PowerShell

# 4. Instalar librerías
pip install -r requirements.txt
```

### Cada vez que abres el proyecto
```bash
# 1. Activar entorno virtual
source venv/Scripts/activate

# 2. Verificar que (venv) aparece en la terminal
```

### Flujo de trabajo diario
```bash
# 1. Hacer cambios en el código
# 2. Añadir cambios
git add .
# 3. Hacer commit con mensaje descriptivo
git commit -m "descripción de lo que hiciste"
# 4. Subir a GitHub
git push
```

---

## Estructura del proyecto
eu-political-observatory/
├── data/
│   ├── raw/          # datos originales — nunca modificar
│   ├── processed/    # datos limpios listos para análisis
│   └── exports/      # outputs para el dashboard
├── docs/             # documentación del proyecto
├── src/
│   ├── ingestion/    # scripts de descarga de datos
│   ├── processing/   # limpieza y transformación
│   ├── analysis/     # modelos, correlaciones, NLP
│   └── api/          # FastAPI
├── notebooks/        # exploración y prototipado
├── tests/            # tests unitarios
├── venv/             # entorno virtual — NO subir a GitHub
├── .cursorrules      # instrucciones para Cursor
├── .gitignore        # archivos ignorados por Git
├── README.md         # descripción del proyecto
└── requirements.txt  # librerías y versiones exactas

---

## Stack técnico
| Componente | Tecnología | Para qué |
|-----------|-----------|---------|
| Backend | Python + FastAPI | Procesar datos y exponer API |
| Base de datos | PostgreSQL | Almacenar datos procesados |
| Frontend | Next.js | Dashboard interactivo |
| Mapas | react-leaflet | Mapas NUTS 2 |
| Gráficas | Recharts | Correlaciones y tendencias |
| NLP | HuggingFace transformers | Análisis de sentimiento político |
| ML | scikit-learn | Modelos correlacionales |
| Deploy | Railway / Render | Hosting gratuito |

---

## Fuentes de datos
| Fuente | Qué contiene | Cobertura |
|--------|-------------|-----------|
| ARDECO | Desempleo, PIB, educación por región NUTS 2 | 1995-2024 |
| EU-NED | Resultados electorales por región NUTS 2 | 1990-2020 |
| POPPA | Scores de populismo y nativismo por partido | 2018, 2023 |
| PopuList | Clasificación far-right/populist | 1989-2022 |
| ESS | Actitudes ciudadanas individuales | Cada 2 años |
| Eurobarometer | Bienestar subjetivo y percepción de amenaza | 2x año |
| Manifesto Project | Discurso político de partidos | Décadas |
| POLAT Panel | Panel longitudinal España | 2010-2020 |
| SOEP | Panel longitudinal Alemania | Décadas |
| ELIPSS | Panel longitudinal Francia | En curso |

---

## Problemas conocidos y soluciones

### Error al instalar pandas en Windows
**Causa:** Python 3.14 no tiene wheels precompilados para pandas.
**Solución:** Usar Python 3.13. Crear el venv con `py -3.13 -m venv venv`.

### Copy-paste en Git Bash no funciona
**Causa:** Git Bash interpreta caracteres especiales al pegar.
**Solución:** Usar la terminal integrada de Cursor (Ctrl+J) o escribir comandos a mano.

### Git init se creó en la carpeta equivocada
**Causa:** Ejecutar `git init` sin estar en la carpeta del proyecto.
**Solución:** `cd` a la carpeta correcta primero, luego `git init`. Verificar con `pwd`.

---

## Cómo actualizar este documento
Cada vez que aprendas algo nuevo, resuelvas un problema, o completes una fase del proyecto, añade una sección aquí. Este documento es un diario técnico del proyecto.