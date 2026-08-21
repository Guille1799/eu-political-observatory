# La línea EFA se retira · 2026-08-21

## Qué se retira

Las dos promesas del tablero de `eu_observatory`:

- `efa-decision` — decidir el nº de factores del EFA (paralelo/MAP, no 12) y tratar los Heywood.
- `efa-rerun` — re-ejecutar el análisis DESPUÉS de decidir, porque los outputs vivos eran del
  17 de mayo, o sea de la solución que la propia promesa decía que estaba mal.

Prometidas el 2026-08-12. Nunca cumplidas: el tablero llevaba **0/2** desde que se escribió.

## Por qué

G, el 2026-08-21, literal: **«efa está descartado ya, hay un proyecto nuevo»**.

No es que la promesa fuera difícil: es que **ya no describe el trabajo**. Un comprobador que
vigila una decisión muerta no es neutro — es peor que no tenerlo. Se queda rojo para siempre,
y un rojo permanente enseña a ignorar los rojos. Ése es exactamente el fallo que el tablero
existía para evitar.

## Qué deja abierto, y es lo importante

Retirar las dos dejaba este tablero **VACÍO**. Y un tablero vacío **no significa «todo hecho»**:
significa que el Stop hook `promesa_gate.py` **falla abierto** en este proyecto, o sea que
cualquier `PRÓXIMO PASO EXACTO` escrito en prosa vuelve a colar aquí. Se perdería en silencio
justo lo que se construyó el 2026-08-21.

Por eso la retirada **no vacía el tablero**: lo sustituye por un único comprobador, `linea-viva`,
que pide por escrito el nombre de la línea nueva. Nace rojo, y su rojo dice la verdad: este repo
no puede prometer nada verificable mientras nadie nombre a qué se dedica ahora.

## Lo que NO se toca

`data/raw/` sigue siendo read-only absoluto, y los outputs de mayo se quedan donde están. Esto
retira una promesa, no borra un análisis.

## Sucesor

**Sin nombrar.** G dijo que hay un proyecto nuevo pero no cuál. Escribirlo aquí de oídas sería
inventar el registro — precisamente lo que estos documentos existen para impedir. Se rellena
cuando él lo diga, creando `docs/decisiones/LINEA_ACTUAL.md` con una línea `linea: <nombre>`.
