# v2 — Trabajo previo: qué está ya hecho, qué no, y qué se puede reutilizar

> **Verificado el 2026-08-17** abriendo las fuentes, no leyendo *sobre* ellas.
> Responde al punto 6 de §7 de [`v2_alcance.md`](v2_alcance.md), que mandaba revisar esto
> **antes de escribir una línea más de fontanería**, porque *"puede ahorrar semanas — o mostrar que
> parte de esto ya está hecho"*.

**Resultado en una línea: el hueco sigue abierto, y lo declaran abierto sus propios dueños.** Hay una
pieza reutilizable (cartografía) y una vía que se descarta con datos (el dataset `renta`).

---

## 1. SEA — Spanish Electoral Archive

**Qué es.** El repositorio público más completo de resultados electorales españoles, en Harvard
Dataverse. Lo mantienen **Jose M. Pavía, Cristina Aybar y Virgilio Pérez** (GIPEyOP, Universitat de
València) y está descrito en un artículo de *Scientific Data* (Nature) de 2021.

🔝 **Detalle que conecta con §8 del alcance:** Pavía y Pérez ya estaban en la lista de *quién actuaría
distinto*. Resulta que además son quienes mantienen el SEA. **El interlocutor y el trabajo previo son
la misma gente**, lo que hace el criterio de impacto bastante más concreto de lo que era.

### 1.1 Estado real, medido hoy (no el que dice el paper)

| Dataset | Última versión | DOI |
|---|---|---|
| Spanish Regional Elections | **9 abr 2026** (V10) | `10.7910/DVN/BJRIXX` |
| Spanish Elections - **Others** | **3 sep 2025** (V6) | `10.7910/DVN/5MMHUI` |
| Spanish European Elections | 8 sep 2024 (V5) | `10.7910/DVN/BXSFUF` |
| Spanish Local Elections | 9 may 2024 (V5) | `10.7910/DVN/53FCE6` |
| Spanish General Elections | **4 ene 2024** (V5) | `10.7910/DVN/0GPRYW` |

⚠️ **No citar el paper de 2021 como estado actual.** Dice *"General (1979–2019)"* y **se ha quedado
viejo**: el dataset de generales incluye `G2023julio_mesas.xlsx` (16,0 MB, publicado 4-ene-2024).
El SEA **sí cubre el 23-J de 2023**, que es la convocatoria que cierra la ventana del ADRH
(2015-2023). Es un error fácil de cometer —fiarse del artículo revisado en vez del repositorio— y
habría descartado el SEA por un motivo falso.

⚠️ **Trampa de formato, anotada para no perder una tarde.** Casi todos los ficheros aparecen como
`.tab` de **182 bytes** con *"1 Variables, 2 Observations"*. **No son los datos**: son la conversión
automática fallida que hace Dataverse del Excel original. Los datos de verdad están en el formato
original (`.xlsx`), y el paquete completo de generales pesa **249,1 MB**.

### 1.2 🔴 El cruce con renta NO existe — y es el hallazgo importante

El dataset **"Spanish Elections - Others"** es, por descripción propia, el que contiene *"nuevas bases
obtenidas por combinación espacial y/o temporal"*. Es decir: **es exactamente donde estaría hecho lo
que v2 quiere hacer.** Contiene **tres ficheros**:

| Fichero | Tamaño | Qué es |
|---|---|---|
| `Cartografia_electoral_generales_2019Abril.rar` | 66,9 MB | Cartografía |
| `Cartografia_electoral_autonomicas_euskadi_2020.rar` | 4,2 MB | Cartografía |
| `Generales_20190428_padron_20190101.tab` | — | Generales abr-2019 × **padrón** 1-ene-2019 |

**El único cruce que existe es electoral × PADRÓN** —población: edad, sexo, nacionalidad— **para una
sola convocatoria**. No hay ningún cruce con renta, ni con el ADRH, ni a varias escalas.

Y no es una omisión: **el propio paper lo declara pendiente**, en el sentido de que una multitud de
variables socioeconómicas a nivel de sección censal, entre ellas los indicadores de renta del INE,
quedan por integrar. **Cinco años después sigue sin integrarse.**

> **Consecuencia para v2:** la pregunta *"¿no estará esto ya hecho?"* tiene respuesta, y es **no**.
> Ni el cruce renta × voto a nivel fino, ni —mucho menos— la comparación entre escalas. Lo que
> existe es la mitad demográfica del cruce, hecha una vez, por el grupo que además es el
> interlocutor natural del resultado.

### 1.3 Qué sí se puede reutilizar

🟢 **La cartografía electoral** (66,9 MB para generales abr-2019). Las geometrías de sección censal
alineadas con las unidades electorales son de lo más caro de construir a mano, y §7-3 del alcance ya
avisa de que la correspondencia entre ficheros cartográficos, electorales y padronales *"no siempre
coincide y varía en el tiempo"* — el SEA lo ha peleado ya.

🟡 **Coste de acceso:** viene en **RAR**, que Python no abre sin binario externo (`unrar`). Y solo
cubre abr-2019 y Euskadi-2020, no toda la serie.

🟡 **Los resultados electorales del SEA son redundantes** con Infoelectoral, que ya se descarga desde
código y es la **fuente primaria**. El SEA sería una fuente derivada. Para procedencia, mejor la
primaria; el SEA vale como **contraste independiente** de que el parseo propio da los mismos números.

---

## 2. El dataset `renta` del paquete `infoelectoral` — se descarta, con cifras

El alcance lo describía como *">34.000 filas ya cruzando renta INE × sección censal"*. **La frase es
literalmente cierta y aun así engañosa**, que es la combinación peligrosa: no es un cruce, es una
tabla de dos columnas.

Reproducible con [`src/v2/auditar_dataset_renta.R`](../src/v2/auditar_dataset_renta.R), que se baja
el paquete de CRAN y lo audita sin instalar nada:

```
Rscript src/v2/auditar_dataset_renta.R
```

| Comprobación | Resultado |
|---|---|
| Forma | 34.680 filas, **2 columnas**: `codigo_seccion` y `renta` (media, €) |
| **Año** | 🔴 **No hay.** Es un corte temporal sin fechar |
| Clave única | 🔴 **No.** 369 filas con código repetido; **207 códigos con dos valores de renta distintos** — p. ej. `1100101001` vale 19.468 **y** 15.618 |
| Cobertura | 🔴 49 provincias de 52. **Falta Araba/Álava**, más Ceuta y Melilla |
| Desigualdad | 🔴 Solo nivel medio. Sin Gini ni P80/P20 |

**Por qué cada fallo mata la vía, y no es quisquillosidad:**

- **Sin año** no se puede cruzar con una convocatoria concreta, ni construir la serie 2015-2023, ni
  saber si la renta es anterior o posterior al voto que se quiere explicar.
- **Clave no única con valores en conflicto**: un `join` por `codigo_seccion` multiplica filas y no
  hay ninguna regla para elegir cuál de los dos valores es el bueno. Se propagaría en silencio.
- **Falta Álava**, y el País Vasco es **caso central del objeto** —el voto a partidos de ámbito no
  estatal—. Perder una de sus tres provincias no es un hueco cualquiera: es un hueco justo donde
  está lo que se estudia. Es la **misma forma de fallo** que mató a v1 (§11: *"la cobertura era peor
  justo donde estaba el objeto"*) y la misma que §6 marca como riesgo que mata el diseño.
- **Sin Gini ni P80/P20** falta la desigualdad, que es una variable distinta del nivel de renta y
  perfectamente puede ser la que importe.

**El ADRH del INE lo domina en las cuatro dimensiones**: 2015-2023 con año, renta + Gini + P80/P20, y
cubre País Vasco y Navarra vía haciendas forales. **Se mantiene el ADRH y se descarta `renta`.**

🟢 **Lo que el paquete `infoelectoral` sí aporta**, y no es poco: `codigos_municipios` (63 KB),
`codigos_partidos`, `codigos_provincias`, `codigos_ccaa` y `fechas_elecciones` — las **tablas de
correspondencia** que §7-3 daba por necesarias, más los lectores `read03`…`read12`, uno por cada
fichero `.DAT` del Ministerio. Eso es **una transcripción independiente del layout** contra la que
contrastar la propia, que es justo lo que hace falta para no volver a suponer una estructura.

---

## 3. Qué cambia esto en el plan

1. **No se descarta ni se adopta el SEA: se usa para lo que sirve.** Cartografía y contraste; los
   resultados salen de Infoelectoral, que es la fuente primaria y ya se baja verificada.
2. **`renta` fuera.** La capa económica es el ADRH.
3. **El hueco está confirmado, no supuesto.** Y confirmado en dos sentidos que se refuerzan: no
   existe el cruce, y quienes tendrían que haberlo hecho lo declaran pendiente por escrito.
4. **Se gana un contraste para el layout**: los lectores `read03`…`read12` de `infoelectoral` son una
   segunda lectura independiente del `FICHEROS.doc` que ya está extraído del zip.

## 4. Lo que NO se ha comprobado, declarado

- **No se ha descargado ni abierto** la cartografía del SEA (66,9 MB en RAR). Que exista y qué cubre
  está verificado; que sea utilizable, **no**.
- **No se ha verificado** si el SEA cubre secciones censales para toda la serie de generales o solo
  para algunas; lo comprobado es que los ficheros se llaman `_mesas` y hay uno por convocatoria.
- **No se ha determinado el año** del dataset `renta`. Se descarta por no declararlo, no por ser de
  un año concreto malo.
- La API de Harvard Dataverse **responde 202 vacío a clientes automáticos**; todo lo de aquí se leyó
  del sitio web. Si se quiere automatizar la descarga, ese muro habrá que resolverlo.
