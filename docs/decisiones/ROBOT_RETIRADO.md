# El robot de este repo se retiró el 2026-09-14 (decisión de G)

> ⚠️ Este repo es PÚBLICO y este fichero se versiona: sin rutas de otros proyectos ni de la máquina. Antes de instalarlo, G lo lee. <!-- EU-17 -->

`eu-political-observatory` se trabaja **a mano**. No hay bucle autónomo aquí y no va a volver.

## Qué se retiró y dónde está lo que valía

Si echas de menos el worktree `eu-ralph` o la rama `ralph/eu`: **no se perdieron, se retiraron a propósito.** Antes se comprobó que estaban vacíos (0 ficheros sucios, 0 commits sin fusionar, `ralph/eu` apuntaba al mismo commit que `main`, `d046faa`) y se salvó a mano todo lo único.

| se retiró | dónde está ahora |
|---|---|
| worktree `eu-ralph` | borrado con `git worktree remove` (salió sin forzar) |
| rama `ralph/eu` | borrada con `git branch -d` (fusionada) |
| 8 × `ralph_run_*.log` del 22-ago | conservados en `logs/ralph-2026-08/`, verificados byte a byte (8/8) |
| reflog de la rama, 36 entradas | volcado a `logs/ralph-2026-08/reflog-ralph-eu.txt` |
| `.env` del worktree | era copia byte a byte del `.env` de la raíz |
| `PENDIENTES.md` del worktree | 3 líneas y ninguna tarea |

Los logs se salvaron porque el `.gitignore` dice de ellos que son «la única crónica de lo que hizo cada noche»; `logs/` sigue ignorado, así que no se publican. **Ningún commit se perdió:** todo el trabajo del robot está dentro de `main`.

## La historia aplastada

El 14-sep se aplastaron 39 commits locales en `d046faa` antes de empujar, porque llevaban rutas absolutas de la máquina y este repo es público. Una rama local `respaldo/antes-del-aplastado-2026-09-14` (`b5eaad7`) guardaba los 39 mensajes; **el 2026-10-23 esa rama ya no existe**, aunque el commit `b5eaad7` sigue en la base de objetos.

## Por qué se llegó a esto

Entre el 21-ago y el 14-sep `main` acumuló 39 commits sin publicar mientras GitHub se quedaba en el 31-ago. **No fue un olvido: fue fricción.** El robot tenía su cuaderno (`PENDIENTES.md`, `PROGRESS.md`) versionado, así que cada tarea marcada como bloqueada era un cambio en un fichero seguido por git, es decir, un commit: los 8 commits `stuck(inv)` tocaban solo esos dos ficheros. Con esa clase de commit dentro, `main` dejaba de ser publicable; publicar exigía peinar la historia; y por eso se posponía. Otro repo público de la casa no diverge nunca por la misma razón inversa: tiene esos dos ficheros en su `.gitignore` versionado desde el principio. Aquí se igualó el 14-sep y, con el robot retirado, la causa desaparece.
