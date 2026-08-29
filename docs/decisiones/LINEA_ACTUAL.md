# La línea de trabajo actual

linea: v2 — ¿dónde ha crecido el voto a VOX en España entre elecciones, y cambia la respuesta según la escala territorial a la que se mire?

> Decidida el 2026-08-16. Sustituye al diseño europeo, que se ejecutó y resultó inviable
> (ver [`../v2_alcance.md`](../v2_alcance.md) §11).
>
> *(Esa línea de arriba empieza por `linea:` y va sin sangrar a propósito: es la única parte de
> este documento pensada para leerse también en automático.)*

## Por qué esto está escrito y no solo entendido

Un repo puede quedarse describiendo un proyecto que ya no existe sin que nadie lo note: el código
sigue compilando, los tests siguen verdes, y la única pieza que ha cambiado —a qué se dedica
esto— no la comprueba nadie. Pasó aquí: durante meses hubo documentos públicos anunciando un
dashboard de partidos nacionalistas en siete países que ya no se estaba construyendo.

Así que la línea viva se declara en un sitio, con fecha, y cuando cambia **se dice por qué**.

## Qué es v2

**La segunda mitad de la pregunta es el producto, no una comprobación.** El mismo dato puede
contar una historia agregado por secciones censales y otra por municipios — el *modifiable areal
unit problem* (MAUP). Junto a ella va la **capa de honestidad**: un mapa que se niega a pintar
donde no hay base, y que dice por qué no pinta.

Dos restricciones del diseño, ambas del 17-ago:

- **El objeto es VOX**, no "partidos de ámbito no estatal". Agregar Euskadi y Cataluña (renta
  alta) con Galicia y Canarias (renta baja) promedia mecanismos contrarios y rompe la variable.
  Con un partido único desaparece además el problema de clasificación, que es **el que mató a v1**.
- **Se mide el CAMBIO entre elecciones, no el nivel en una.** "Auge" es un cambio, y medirlo solo
  es posible con un partido estable: comparar el mismo sitio consigo mismo resta todo lo que de
  ese sitio no cambia.

**Antecedente directo:** Roig, Espinosa & Pavía (2025), *Frontiers in Political Science*. Usan las
mismas dos fuentes, concluyen que a VOX lo trajo la renta media-alta, y justifican el uso de la
sección censal por su homogeneidad interna — sin comprobar en ningún momento si el resultado
sobrevive a cambiar de unidad. Ese hueco es el que ocupa esta línea.

**Fuentes:** Infoelectoral (Ministerio del Interior) y el Atlas de distribución de renta de los
hogares (INE).

## Lo que NO es la línea

El **pipeline ESS está congelado**, no borrado: sus scripts y sus resultados siguen donde estaban,
simplemente ya no describen el trabajo en curso. El motivo está en
[`EFA_RETIRADO_2026-08-21.md`](EFA_RETIRADO_2026-08-21.md). `data/raw/` sigue siendo de solo
lectura.

## Cómo se actualiza esto

Cuando la línea cambie otra vez, se reescribe la línea `línea:` de arriba **y se explica aquí por
qué**. Lo primero es lo que se lee; lo segundo es lo que sirve al siguiente que llegue.
