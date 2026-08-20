"""
v2 -- Que candidaturas de VOX existieron en cada general, y si fueron en coalicion.

Por que esto se puede mirar sin contaminar el preregistro
---------------------------------------------------------
Lee UNICAMENTE el fichero `03`, el catalogo de candidaturas: codigo, siglas y
denominacion. **Cero votos.** Saber que candidaturas se presentaron no dice nada
sobre quien gano; los resultados viven en los ficheros 06/08/10 y aqui no se
tocan. Por eso este paso puede ir antes de escribir la regla de coaliciones, y no
al reves.

Que se busca
------------
1. Cuantas veces VOX concurrio en coalicion, que es el tamanio del problema. La
   regla se elige DESPUES de saberlo, igual que se hizo con el umbral del 30% en
   `supervivencia_secciones.py`.
2. Si el propio Ministerio ya declara la agrupacion. El fichero `03` trae, por
   candidatura, el codigo de la **candidatura cabecera de acumulacion** a nivel
   provincial, autonomico y nacional. Si eso esta bien puesto, no hay que
   inventar criterio: se lee el suyo y se decide si se acepta.

Alcance: SOLO GENERALES (§5.7 del alcance), las cinco de la ventana del Atlas de
renta: 2015-12, 2016-06, 2019-04, 2019-11 y 2023-07.

Uso:  python src/v2/catalogo_vox.py
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from descarga_infoelectoral import TIPO_CONGRESO, descargar, url_de  # noqa: E402
from layout_infoelectoral import esquema_de_zip  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
EXTERNAL = RAIZ / "data" / "external" / "infoelectoral"

GENERALES = ((2015, 12), (2016, 6), (2019, 4), (2019, 11), (2023, 7))
AGUJA = "VOX"


def zip_de(anio, mes):
    url = url_de(TIPO_CONGRESO, anio, mes, "MESA")
    destino = EXTERNAL / Path(url).name
    ok, detalle = descargar(url, destino)
    if not ok:
        print("[%d-%02d] FALLO: %s" % (anio, mes, detalle))
    return destino if ok else None


def candidaturas(ruta_zip, anio, mes):
    """Devuelve la lista de candidaturas del fichero 03 como diccionarios."""
    f03 = esquema_de_zip(ruta_zip)["03"]
    campos = {
        "codigo": f03.campo("Código de la candidatura"),
        "siglas": f03.campo("Siglas"),
        "denominacion": f03.campo("Denominación"),
        "cab_prov": f03.campo("nivel provincial"),
        "cab_auto": f03.campo("nivel autonómico"),
        "cab_nac": f03.campo("nivel nacional"),
    }
    with zipfile.ZipFile(ruta_zip) as z:
        datos = z.read(f03.nombre_fichero(TIPO_CONGRESO, anio, mes))
    filas = []
    for linea in datos.split(b"\n")[:-1]:
        r = linea.decode("cp1252")
        filas.append({k: r[c.rebanada].strip() for k, c in campos.items()})
    return filas


def main():
    for anio, mes in GENERALES:
        ruta = zip_de(anio, mes)
        if ruta is None:
            continue
        filas = candidaturas(ruta, anio, mes)
        # La aguja se busca en siglas Y en denominacion: si VOX va en coalicion,
        # las siglas pueden ser las del pacto y VOX aparecer solo en el nombre largo.
        hits = [
            f for f in filas
            if AGUJA in f["siglas"].upper() or AGUJA in f["denominacion"].upper()
        ]
        siglas = sorted({f["siglas"] for f in hits})
        denoms = sorted({f["denominacion"] for f in hits})
        cabeceras = sorted({f["cab_nac"] for f in hits})
        print()
        print("GENERALES %d-%02d  ·  %d candidaturas en total  ·  %d mencionan %s"
              % (anio, mes, len(filas), len(hits), AGUJA))
        print("   siglas distintas      : %s" % siglas)
        print("   nombres distintos     : %s" % denoms)
        print("   cabeceras nacionales  : %s" % cabeceras)
        # Lo unico que hay que mirar a mano: candidaturas cuyo nombre NO sea
        # exactamente la aguja, que son las candidatas a ser coalicion.
        raros = [f for f in hits if f["denominacion"].upper() != AGUJA]
        if raros:
            print("   >>> %d candidaturas con nombre distinto de %r:" % (len(raros), AGUJA))
            for f in raros:
                print("       %s | %s | %s | cab.nac=%s"
                      % (f["codigo"], f["siglas"], f["denominacion"], f["cab_nac"]))
        else:
            print("   >>> ninguna candidatura con nombre distinto: VOX concurrio SOLA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
