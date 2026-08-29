"""
Tests de la deteccion de particiones ocultas.

Se prueban con secciones inventadas, no con los ficheros reales, y a proposito: lo
que hay que validar aqui no es que los datos se lean -- de eso ya se encarga
`test_layout_infoelectoral.py` -- sino que la REGLA distingue las dos historias
que producen el mismo sintoma:

  - Getafe: la seccion se partio. Pierde censo Y nace una hermana en su distrito.
            Nos rompe la comparacion, porque ya no es el mismo trozo de mapa.
  - Soria:  la seccion se vacio. Pierde censo y NO nace nadie.
            NO nos rompe nada: mismo mapa, menos gente. Es un cambio real.

Confundirlas en cualquiera de los dos sentidos es un error caro y silencioso, asi
que cada caso tiene su test, incluidos los feos: el limite exacto del umbral, la
hermana que nace en OTRO distrito, y el censo cero.
"""

import json
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from descarga_infoelectoral import TIPO_CONGRESO
from layout_infoelectoral import esquema_de_zip, lineas_de_registro
from supervivencia_secciones import (
    EXTERNAL,
    MUNICIPIO_NO_TERRITORIAL,
    PROCESADO,
    PROVINCIA_NO_TERRITORIAL,
    UMBRAL_PRINCIPAL,
    UMBRALES_SENSIBILIDAD,
    censo_por_seccion,
    fusiones_ocultas,
    particiones_ocultas,
)

RAIZ = Path(__file__).resolve().parents[2]

# Las tres convocatorias que `supervivencia_secciones.main()` necesita para comparar
# (CONTROL = 2019-04 -> 2019-11, REAL = 2019-11 -> 2023-07). Si falta alguna, `main()`
# NO falla: se pone a DESCARGARLA del Ministerio. Eso no puede pasar dentro de la suite
# —convertiria `pytest src` en una descarga de cientos de MB sin avisar—, asi que el
# test se salta y dice como conseguir los ficheros, igual que hace test_layout.
CONVOCATORIAS_NECESARIAS = ((2019, 4), (2019, 11), (2023, 7))
ZIPS_NECESARIOS = [
    RAIZ / "data" / "external" / "infoelectoral" / ("02%d%02d_MESA.zip" % (anio, mes))
    for anio, mes in CONVOCATORIAS_NECESARIAS
]
necesita_las_tres = pytest.mark.skipif(
    not all(z.exists() for z in ZIPS_NECESARIOS),
    reason="faltan convocatorias -- bajalas con: %s"
    % "; ".join(
        "python src/v2/descarga_infoelectoral.py %d %d" % c for c in CONVOCATORIAS_NECESARIAS
    ),
)

# (provincia, municipio, distrito, seccion)
MADRE = ("28", "065", "01", "001")
HERMANA = ("28", "065", "01", "015")
OTRO_DISTRITO = ("28", "065", "02", "007")
VECINA = ("28", "065", "01", "002")


def test_getafe_la_seccion_se_partio():
    """Pierde la mitad del censo y nace una hermana en su distrito."""
    antes = {MADRE: 3000}
    despues = {MADRE: 1500, HERMANA: 1500}
    ocultas, solo_encogen = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas == {MADRE}
    assert solo_encogen == set()


def test_soria_la_seccion_se_vacio():
    """Pierde la mitad del censo pero no nace nadie: es despoblacion real."""
    antes = {MADRE: 3000}
    despues = {MADRE: 1500}
    ocultas, solo_encogen = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas == set()
    assert solo_encogen == {MADRE}


def test_una_seccion_estable_no_es_ninguna_de_las_dos():
    antes = {MADRE: 3000}
    despues = {MADRE: 2950, HERMANA: 800}
    ocultas, solo_encogen = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas == set()
    assert solo_encogen == set()


def test_la_hermana_tiene_que_nacer_en_SU_distrito():
    """Una seccion nueva en otro distrito no explica que esta encogiera."""
    antes = {MADRE: 3000}
    despues = {MADRE: 1500, OTRO_DISTRITO: 1500}
    ocultas, solo_encogen = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas == set(), "una hermana de otro distrito no puede ser la causa"
    assert solo_encogen == {MADRE}


def test_una_hermana_ya_existente_no_cuenta_como_nueva():
    """Solo explica la caida una seccion que NO estaba antes."""
    antes = {MADRE: 3000, VECINA: 900}
    despues = {MADRE: 1500, VECINA: 900}
    ocultas, solo_encogen = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas == set()
    assert solo_encogen == {MADRE}


def test_el_limite_exacto_del_umbral_cuenta_como_caida():
    """Perder exactamente el umbral entra. El caso de borde se fija, no se deja al azar."""
    antes = {MADRE: 1000}
    despues = {MADRE: 700, HERMANA: 300}  # -30% exacto
    ocultas, _ = particiones_ocultas(antes, despues, 0.30)
    assert ocultas == {MADRE}

    justo_por_encima = {MADRE: 701, HERMANA: 299}  # -29,9%
    ocultas, _ = particiones_ocultas(antes, justo_por_encima, 0.30)
    assert ocultas == set()


def test_un_censo_de_partida_cero_no_revienta_ni_cuenta():
    """Sin censo en el origen no hay proporcion; se ignora en vez de dividir por cero."""
    antes = {MADRE: 0}
    despues = {MADRE: 0, HERMANA: 10}
    ocultas, solo_encogen = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas == set()
    assert solo_encogen == set()


def test_una_seccion_muerta_no_aparece_en_ninguno_de_los_dos_grupos():
    """Las muertas se cuentan aparte: aqui solo entran las que sobreviven de codigo."""
    antes = {MADRE: 3000}
    despues = {HERMANA: 3000}
    ocultas, solo_encogen = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas == set()
    assert solo_encogen == set()


@pytest.mark.parametrize("umbral", [0.20, 0.30, 0.40, 0.50])
def test_un_umbral_mas_exigente_nunca_encuentra_mas_particiones(umbral):
    """Monotonia: subir el liston no puede aumentar el recuento."""
    antes = {MADRE: 1000, VECINA: 1000}
    despues = {MADRE: 750, VECINA: 400, HERMANA: 850}
    ocultas, _ = particiones_ocultas(antes, despues, umbral)
    mas_laxo, _ = particiones_ocultas(antes, despues, 0.10)
    assert ocultas <= mas_laxo


def test_una_fusion_tambien_rompe_la_identidad():
    """El caso simetrico de Getafe: MADRE absorbe a HERMANA, que muere.

    particiones_ocultas no lo ve -- MADRE ni se parte ni encoge -- pero el
    trozo de mapa detras de su codigo ya no es el mismo.
    """
    antes = {MADRE: 1500, HERMANA: 1500}
    despues = {MADRE: 3000}

    ocultas, solo_encogen = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas == set()
    assert solo_encogen == set()

    fusiones, solo_crecen = fusiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert fusiones == {MADRE}
    assert solo_crecen == set()


FUSIONES_ESPERADAS = {0.20: 268, 0.30: 238, 0.40: 218, 0.50: 190}


def test_las_fusiones_reales_de_2019_a_2023_se_cuentan():
    """Cifras pinchadas sobre los .DAT reales de 2019-11 y 2023-07."""
    antes = censo_por_seccion(EXTERNAL / "02201911_MESA.zip", 2019, 11)
    despues = censo_por_seccion(EXTERNAL / "02202307_MESA.zip", 2023, 7)

    for umbral, esperadas in FUSIONES_ESPERADAS.items():
        fusiones, _ = fusiones_ocultas(antes, despues, umbral)
        assert len(fusiones) == esperadas, "umbral %.2f" % umbral

    ocultas, _ = particiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert len(ocultas) == 304

    fusiones, _ = fusiones_ocultas(antes, despues, UMBRAL_PRINCIPAL)
    assert ocultas & fusiones == set()

    sobreviven = antes.keys() & despues.keys()
    identidad_real = len(sobreviven) - len(ocultas | fusiones)
    assert identidad_real == 35492


@necesita_las_tres
def test_el_json_de_salida_declara_las_fusiones():
    """`python src/v2/supervivencia_secciones.py` tiene que ESCRIBIR el JSON."""
    script = Path(__file__).resolve().parent / "supervivencia_secciones.py"
    resultado = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        # En Windows, pytest sustituye sys.stdin por un objeto sin descriptor real. Sin
        # esto, subprocess intenta heredarlo y revienta con "[WinError 6] The handle is
        # invalid" -- que ademas solo aparece en la tanda completa, no al correr el test
        # suelto, o sea el peor tipo de fallo: el que no se reproduce cuando lo miras.
        stdin=subprocess.DEVNULL,
        text=True,
        cwd=Path(__file__).resolve().parents[2],
    )
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
    assert PROCESADO.exists()

    datos = json.loads(PROCESADO.read_text(encoding="utf-8"))
    real = datos["REAL"]

    for umbral, esperadas in FUSIONES_ESPERADAS.items():
        assert real["umbrales"][str(umbral)]["fusiones"] == esperadas, "umbral %.2f" % umbral

    umbral_principal = real["umbrales"][str(UMBRAL_PRINCIPAL)]
    assert umbral_principal["ocultas"] == 304
    assert umbral_principal["fusiones"] == 238
    assert umbral_principal["identidad_real"] == 35492
    assert (umbral_principal["identidad_real"]
            == real["sobreviven"] - (umbral_principal["ocultas"] + umbral_principal["fusiones"]))


def _suma_censo(esquema, ruta_zip, codigo_fichero, anio, mes, filtro):
    """Suma el campo Censo del I.N.E. de un fichero de ancho fijo, filas que pasen `filtro`."""
    fichero = esquema[codigo_fichero]
    censo = fichero.campo("Censo del I.N.E")
    with zipfile.ZipFile(ruta_zip) as z:
        datos = z.read(fichero.nombre_fichero(TIPO_CONGRESO, anio, mes))
    total = 0
    for linea in lineas_de_registro(datos)[:-1]:
        r = linea.decode("cp1252")
        if filtro(fichero, r):
            total += int(r[censo.rebanada])
    return total


def test_censo_por_seccion_cuadra_con_el_total_nacional():
    """El territorial (09, filtrado) mas el C.E.R.A. (09, lo excluido) cuadra con el 07.

    Es la comprobacion barata que el docstring de censo_por_seccion describe y que
    ningun test ejercia: romper el filtro de PROVINCIA_NO_TERRITORIAL/
    MUNICIPIO_NO_TERRITORIAL infla el censo (cuela filas de C.E.R.A. y de totales)
    y esta suma deja de cuadrar con el censo nacional que trae el propio fichero 07
    ('DATOS COMUNES DE AMBITO SUPERIOR AL MUNICIPIO', fila Total Nacional).
    """
    ruta = EXTERNAL / "02201911_MESA.zip"
    esquema = esquema_de_zip(ruta)

    territorial = sum(censo_por_seccion(ruta, 2019, 11).values())
    assert territorial == 34870481

    f09 = esquema["09"]
    prov09, muni09 = f09.campo("Código I.N.E. de la provincia"), f09.campo("del municipio")
    cera = _suma_censo(
        esquema, ruta, "09", 2019, 11,
        lambda f, r: (r[prov09.rebanada] != PROVINCIA_NO_TERRITORIAL
                      and r[muni09.rebanada] == MUNICIPIO_NO_TERRITORIAL),
    )
    assert cera == 2130754

    f07 = esquema["07"]
    ccaa07, prov07 = f07.campo("Comunidad Autónoma"), f07.campo("de la provincia")
    nacional = _suma_censo(
        esquema, ruta, "07", 2019, 11,
        lambda f, r: r[ccaa07.rebanada] == "99" and r[prov07.rebanada] == "99",
    )
    assert nacional == 37001235

    assert territorial + cera == nacional
