"""
v2 -- Cuantas secciones censales sobreviven entre convocatorias, y cuantas
sobreviven solo de nombre.

Por que esto va antes que nada
------------------------------
El diseno de v2 mide el CAMBIO del voto a VOX: el mismo sitio comparado consigo
mismo en dos elecciones. Eso exige que el sitio EXISTA en las dos. Y la seccion
censal -- el peldano mas fino de la escalera, y la mitad del producto -- se
redibuja cuando cambia su poblacion: el INE la parte si crece y la fusiona si se
vacia.

El riesgo no es de limpieza, es de diseno, y ademas apunta en la direccion del
resultado que se busca: las fronteras de MUNICIPIO casi no se mueven y las de
SECCION si, asi que una diferencia entre esas dos escalas podria ser ruido de
fronteras disfrazado de "efecto de escala".

Las dos medidas, y por que hacen falta las dos
----------------------------------------------
1) SUPERVIVENCIA DE CODIGO. Cuantas secciones conservan su codigo entre dos
   convocatorias. Es la medida obvia, y es un TECHO: conservar el codigo no
   garantiza que la frontera no se tocara.

2) PARTICIONES OCULTAS. El caso que (1) no ve, y es el peligroso: cuando una
   seccion se parte, lo natural es que una mitad conserve el codigo del padre y
   la otra reciba uno nuevo. Para (1) esa seccion "sobrevive", cuando en realidad
   ha perdido medio cuerpo.

   Se detecta pidiendo DOS cosas a la vez, porque ninguna vale sola:
     a) que el censo caiga fuerte -- una particion se lleva de golpe parte de los
        vecinos; y
     b) que en su mismo municipio y distrito haya nacido una seccion nueva.
   Solo (a) confunde particion con despoblacion real, que en el interior existe.
   Solo (b) no dice a quien se partio.

El control, que es lo que hace creible todo lo demas
----------------------------------------------------
Todo se calcula DOS veces:
  A) 2019-04 -> 2019-11   (6 meses)   CONTROL
  B) 2019-11 -> 2023-07   (3 anios y 8 meses)   la pregunta de verdad

En seis meses el INE apenas retoca nada, asi que A tiene que salir casi perfecto.
Si A saliera mal, lo roto seria la medicion y no el pais. Sin ese control, un
resultado raro en B no se podria atribuir: mundo o error propio, sin distinguir.

Umbral
------
UMBRAL_PRINCIPAL = 0.30 (perder el 30% del censo o mas cuenta como caida fuerte).
Elegido CON G y ANTES de mirar los datos, el 2026-08-19, con este razonamiento:
una particion en dos suele llevarse cerca de la mitad, y un barrio que se vacia de
verdad rara vez pierde un tercio de sus vecinos en cuatro anios. Es un juicio, no
una ley -- por eso el resultado se reporta ademas a otros umbrales, para que se
vea si la conclusion depende de donde se puso la raya.

Uso:  python src/v2/supervivencia_secciones.py     (desde cualquier sitio)
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

CONTROL = ((2019, 4), (2019, 11))
REAL = ((2019, 11), (2023, 7))

# Codigos que no son un sitio: voto exterior (C.E.R.A.) y filas de totales.
PROVINCIA_NO_TERRITORIAL = "99"
MUNICIPIO_NO_TERRITORIAL = "999"

UMBRAL_PRINCIPAL = 0.30
UMBRALES_SENSIBILIDAD = (0.20, 0.30, 0.40, 0.50)


def zip_de(anio, mes):
    """Baja el ambito MESA de una convocatoria (o lo reutiliza si ya esta)."""
    url = url_de(TIPO_CONGRESO, anio, mes, "MESA")
    destino = EXTERNAL / Path(url).name
    ok, detalle = descargar(url, destino)
    print("[%d-%02d] %s: %s" % (anio, mes, "OK" if ok else "FALLO", detalle))
    return destino if ok else None


def censo_por_seccion(ruta_zip, anio, mes):
    """{(provincia, municipio, distrito, seccion): censo} de una convocatoria.

    El fichero 09 da una fila por MESA, asi que el censo de la seccion es la suma
    de las mesas que contiene.

    La especificacion se lee DE ESE zip, no del de otro anio: si el Ministerio
    cambio el formato, el esquema se adapta solo -- y si cambio tanto que ya no
    encuentra un campo, revienta con un error claro en vez de leer basura.
    """
    esquema = esquema_de_zip(ruta_zip)
    f09 = esquema["09"]
    prov = f09.campo("de la provincia")
    muni = f09.campo("del municipio")
    dist = f09.campo("distrito municipal")
    secc = f09.campo("de la sección")
    censo = f09.campo("Censo del I.N.E")

    with zipfile.ZipFile(ruta_zip) as z:
        datos = z.read(f09.nombre_fichero(TIPO_CONGRESO, anio, mes))

    por_seccion = {}
    for linea in datos.split(b"\n")[:-1]:
        r = linea.decode("cp1252")
        p, m = r[prov.rebanada], r[muni.rebanada]
        if p == PROVINCIA_NO_TERRITORIAL or m == MUNICIPIO_NO_TERRITORIAL:
            continue
        clave = (p, m, r[dist.rebanada], r[secc.rebanada])
        por_seccion[clave] = por_seccion.get(clave, 0) + int(r[censo.rebanada])
    return por_seccion


def particiones_ocultas(antes, despues, umbral):
    """Secciones que conservan el codigo pero encogen y tienen hermana nueva.

    Devuelve (ocultas, solo_encogen). La segunda son las que caen fuerte SIN que
    nazca nadie a su lado: candidatas a despoblacion real, no a particion.
    """
    sobreviven = antes.keys() & despues.keys()
    nacen = despues.keys() - antes.keys()
    distritos_con_hermana_nueva = {s[:3] for s in nacen}

    ocultas, solo_encogen = set(), set()
    for s in sobreviven:
        if antes[s] == 0:
            continue  # sin censo de partida no hay proporcion que calcular
        if despues[s] > (1 - umbral) * antes[s]:
            continue
        if s[:3] in distritos_con_hermana_nueva:
            ocultas.add(s)
        else:
            solo_encogen.add(s)
    return ocultas, solo_encogen


def informe(etiqueta, antes, despues, origen, destino):
    sobreviven = antes.keys() & despues.keys()
    mueren = antes.keys() - despues.keys()
    nacen = despues.keys() - antes.keys()

    print()
    print("=" * 72)
    print("%s   %s  ->  %s" % (etiqueta, origen, destino))
    print("=" * 72)
    print("  secciones en %s : %6d" % (origen, len(antes)))
    print("  secciones en %s : %6d" % (destino, len(despues)))
    print("  sobreviven (codigo): %6d   (%.2f%% de las de %s)"
          % (len(sobreviven), 100 * len(sobreviven) / len(antes), origen))
    print("  mueren             : %6d   (%.2f%%)"
          % (len(mueren), 100 * len(mueren) / len(antes)))
    print("  nacen              : %6d" % len(nacen))

    print()
    print("  particiones ocultas (encoge Y nace hermana en su distrito):")
    print("    %-8s  %-10s  %-10s  %s" % ("umbral", "ocultas", "solo encogen", "identidad real"))
    for u in UMBRALES_SENSIBILIDAD:
        ocultas, solo = particiones_ocultas(antes, despues, u)
        intactas = len(sobreviven) - len(ocultas)
        marca = "  <-- umbral acordado" if abs(u - UMBRAL_PRINCIPAL) < 1e-9 else ""
        print("    -%2d%%      %-10d  %-10d  %6d  (%.2f%% de %s)%s"
              % (100 * u, len(ocultas), len(solo), intactas,
                 100 * intactas / len(antes), origen, marca))


def main():
    convocatorias = sorted({*CONTROL, *REAL})
    censos = {}
    for anio, mes in convocatorias:
        ruta = zip_de(anio, mes)
        if ruta is None:
            print("  -> sin fichero, no se puede comparar. Se aborta.")
            return 1
        censos[(anio, mes)] = censo_por_seccion(ruta, anio, mes)

    def eti(c):
        return "%d-%02d" % c

    informe("CONTROL", censos[CONTROL[0]], censos[CONTROL[1]],
            eti(CONTROL[0]), eti(CONTROL[1]))
    informe("REAL   ", censos[REAL[0]], censos[REAL[1]],
            eti(REAL[0]), eti(REAL[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
