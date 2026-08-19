# hooks/ — los git hooks del proyecto, versionados

Los hooks de git viven por defecto en `.git/hooks/`, que **no viaja con el repo**: no se
clona, no se revisa en un diff y no sobrevive a un clon nuevo. Esta carpeta existe para que
el contenido del hook sea del proyecto y no de una máquina.

## Activarlo (una vez por clon)

```bash
bash hooks/install.sh
```

Es equivalente a `git config core.hooksPath hooks`.

**Git no puede hacer esto por ti, y es a propósito:** si clonar un repo activara
automáticamente sus scripts, clonar código ajeno sería ejecutar código ajeno. Por eso
versionar el hook resuelve *el contenido* (uno solo, visible, revisable) pero **no la
activación**: eso sigue siendo un paso por clon. Lo que sí cambia es que ahora ese paso es
un comando documentado, y no reescribir un fichero invisible de memoria.

Para comprobar si está activo en este clon:

```bash
git config --get core.hooksPath
```

## Rutas locales

Dos checks llaman a herramientas que viven fuera del repo. Sus rutas **no** están
codificadas en el hook — se leen de la config del clon, con el layout de la máquina de
origen como valor por defecto:

```bash
git config hooks.vigilanteRepo "/ruta/a/capa-normativa"
git config hooks.secretScan    "/ruta/a/vigilante_pre_commit.py"
```

## Qué comprueba `pre-commit`

| Check | Qué bloquea | Si la herramienta no está |
|---|---|---|
| 1 · Metodología R | `lrscale` entrando en el EFA (circularidad); escrituras en `data/raw/` | n/a — es grep, sin dependencias |
| 2 · Sintaxis Python | cualquier `.py` versionado que no parsee | cae a `ast.parse` inline sobre lo que esté en stage |
| 3 · Credenciales | secretos en ficheros versionados | **bloquea** — un escáner ausente no es un escáner limpio |

El Check 2 existe por un caso real: un `SyntaxError` estuvo **dos meses** commiteado en
`src/ingestion/load_ardeco.py` sin que ninguno de los mecanismos de solidez del repo lo
viera. Ninguno de los tres checks falla en abierto: un guard que desaparece en silencio es
peor que no tener guard, porque además da tranquilidad.

## Tocar el hook

Edita `hooks/pre-commit` y commitéalo. No edites `.git/hooks/pre-commit`: con
`core.hooksPath` apuntando aquí, esa carpeta ya no se ejecuta, y un cambio ahí sería una
edición silenciosa que no le llega a nadie.

Después de cambiarlo, **verifícalo por mutación, no leyéndolo**: planta un fichero que
viole la regla, comprueba que el commit se bloquea, y comprueba también que sin él pasa
limpio. Un guard que nunca has visto fallar no sabes si funciona.
