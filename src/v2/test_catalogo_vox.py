"""
Tests del catalogo de candidaturas de VOX (fichero 03), en las cinco generales.

Que se prueba
-------------
`catalogo_vox.candidaturas()` lee el fichero 03 tal cual, siglas y cabeceras de
acumulacion incluidas. La regla que importa vive en `separar_cabeceras()`: una
cabecera de acumulacion (el "904688" de 2015-12, que agrupa las 30 listas
provinciales de VOX) no es una candidatura mas, y contarla como tal triplica
la cifra de concurrencia territorial que el modulo existe para medir.

Se corre sobre los cinco *_MESA.zip ya descargados en data/external/, no sobre
datos inventados: la cifra exacta (30 candidaturas + 1 cabecera en 2015-12, y
1 + 0 en las otras cuatro) solo sale de leer el fichero 03 real.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from catalogo_vox import GENERALES, candidaturas, separar_cabeceras, zip_de  # noqa: E402

# (anio, mes) -> (candidaturas reales de VOX, cabeceras de acumulacion)
ESPERADO = {
    (2015, 12): (30, 1),
    (2016, 6): (1, 0),
    (2019, 4): (1, 0),
    (2019, 11): (1, 0),
    (2023, 7): (1, 0),
}


def _hits(filas, aguja="VOX"):
    return [f for f in filas if aguja in f["siglas"].upper() or aguja in f["denominacion"].upper()]


@pytest.mark.parametrize("anio,mes", GENERALES)
def test_candidaturas_de_vox_y_cabeceras_de_acumulacion(anio, mes):
    ruta = zip_de(anio, mes)
    filas = candidaturas(ruta, anio, mes)
    reales, cabeceras = separar_cabeceras(_hits(filas), filas)
    assert (len(reales), len(cabeceras)) == ESPERADO[(anio, mes)]


def test_2015_la_cabecera_es_904688_y_no_una_de_las_30_provinciales():
    """El criterio no puede ser `codigo == cab_nac`: en 2016+ la candidatura
    unica tambien se autoreferencia asi (ver test de abajo) y no es cabecera."""
    ruta = zip_de(2015, 12)
    filas = candidaturas(ruta, 2015, 12)
    reales, cabeceras = separar_cabeceras(_hits(filas), filas)
    assert {f["codigo"] for f in cabeceras} == {"904688"}
    assert "904688" not in {f["codigo"] for f in reales}


def test_una_candidatura_unica_no_es_su_propia_cabecera():
    """2016-06: codigo == cab_prov == cab_auto == cab_nac ('000094'), pero es
    la unica fila de VOX -- nadie mas la referencia -- asi que no es una
    cabecera de acumulacion, solo una candidatura sin reparto que acumular."""
    ruta = zip_de(2016, 6)
    filas = candidaturas(ruta, 2016, 6)
    hits = _hits(filas)
    assert len(hits) == 1
    assert hits[0]["codigo"] == hits[0]["cab_nac"] == "000094"
    reales, cabeceras = separar_cabeceras(hits, filas)
    assert reales == hits
    assert cabeceras == []


def test_los_codigos_se_reasignan_entre_convocatorias():
    """Ningun codigo identifica al mismo partido entre convocatorias: '000116'
    es VOX en 2019-11 y VOU (Vivir Ourense) en 2019-04. Es la razon por la que
    `catalogo_vox` identifica por SIGLAS dentro de cada convocatoria, nunca por
    codigo entre convocatorias."""
    filas_1911 = {f["codigo"]: f for f in candidaturas(zip_de(2019, 11), 2019, 11)}
    filas_1904 = {f["codigo"]: f for f in candidaturas(zip_de(2019, 4), 2019, 4)}
    assert filas_1911["000116"]["siglas"] == "VOX"
    assert filas_1904["000116"]["siglas"] == "VOU"
    assert filas_1904["000116"]["denominacion"] == "VIVIR OURENSE"
