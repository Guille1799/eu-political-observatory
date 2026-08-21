# La línea de trabajo actual de este repo

linea: v2 — ¿dónde ha CRECIDO el voto a VOX en España entre elecciones, y cambia la respuesta según la escala territorial?

## Por qué hace falta decir esto por escrito

El 2026-08-21 se retiraron las dos promesas de EFA (`efa-decision`, `efa-rerun`): G dijo
«efa está descartado ya, hay un proyecto nuevo». El motivo y la retirada están en
`EFA_RETIRADO_2026-08-21.md`.

Pero retirarlas dejaba el tablero **vacío**, y un tablero vacío no significa «todo hecho»:
significa que el Stop hook `promesa_gate.py` **falla abierto** aquí, o sea que cualquier
`PRÓXIMO PASO EXACTO` escrito en prosa vuelve a colar en este repo. Este fichero tapa ese
agujero, y `aceptacion.py linea-viva` lo vigila.

## Qué es v2 (decidida el 2026-08-16, según `docs/EU_REFERENCIA_CORE.md`)

La segunda mitad de la pregunta **es el producto**, no un chequeo: el mismo dato puede contar
una historia agregado por secciones censales y otra por municipios — el *modifiable areal unit
problem* (MAUP). Junto a ella va la **capa de honestidad**: un mapa que se niega a pintar donde
no hay base, y lo dice.

Dos restricciones que hay que respetar, del 17-ago:

- **El objeto es VOX, no PANE.** Agregar Euskadi/Cataluña (renta alta) con Galicia/Canarias
  (renta baja) promedia mecanismos contrarios y rompe la variable. Con un partido único
  desaparece además el problema de clasificación, que es el que mató a v1.
- **Se mide el CAMBIO entre elecciones, no el nivel en una.** «Auge» es un cambio, y solo es
  posible con un partido estable: comparar el mismo sitio consigo mismo resta lo que no cambia.

**Diana con nombre:** Roig, Espinosa & Pavía (2025), *Frontiers in Political Science*. Usan las
mismas dos fuentes, concluyen que a VOX lo trajo la renta media-alta, justifican la sección
censal por su homogeneidad interna — y no mencionan el MAUP ni una vez. Dos de los tres huecos
los piden ellos mismos; el tercero es su omisión.

**Fuentes:** Infoelectoral (Mº Interior) y el Atlas de distribución de renta de los hogares (INE).

## Lo que NO es la línea

El **pipeline ESS está CONGELADO**, no borrado. Sus scripts y sus outputs de mayo siguen donde
están; simplemente ya no describen el trabajo. `data/raw/` sigue siendo read-only absoluto.

## Cómo se actualiza esto

Cuando la línea cambie otra vez, se reescribe la línea `linea:` **y se dice aquí por qué**. El
comprobador solo exige que exista y nombre algo; el porqué es para el siguiente que llegue.
