# El análisis factorial (EFA) se retira · 2026-08-21

## Qué se retira

Dos compromisos que estaban abiertos sobre el pipeline ESS:

- **decidir el número de factores** del EFA (paralelo / MAP, no los 12 que salían por defecto) y
  tratar los casos Heywood;
- **re-ejecutar el análisis después** de esa decisión, porque los resultados que había vivos eran
  del 17 de mayo — es decir, de la misma solución que el primer compromiso reconocía como mala.

Ninguno de los dos se cumplió: llevaban abiertos desde el 2026-08-12.

## Por qué se retiran

No porque fueran difíciles, sino porque **ya no describían el trabajo**. El 2026-08-21 la línea del
repo pasó a ser otra (ver [`LINEA_ACTUAL.md`](LINEA_ACTUAL.md)), y arrastrar un pendiente que
apunta a un análisis que nadie va a continuar es peor que no tenerlo: se queda ahí para siempre, y
un aviso que lleva meses en rojo deja de leerse. Es exactamente el fallo que llevar registro de
decisiones existe para evitar.

## Qué NO se retira

**El análisis no se borra: se congela.** Los scripts de `R/ess_spain/` siguen donde están y siguen
siendo ejecutables, y los resultados de mayo se conservan. `data/raw/` sigue siendo de solo lectura.

Y el problema de fondo tampoco se declara resuelto. El EFA exploratorio devolvió una **solución
impropia (caso Heywood)** y ese sigue siendo su estado. Está dicho tal cual en
[`R/README.md`](../../R/README.md): el modelo de medida **no está cerrado**, y no se afirma lo
contrario en ninguna parte del repo.

Lo que cambia es su papel: era el camino principal, y pasa a ser una capa parada que la línea
actual no necesita.
