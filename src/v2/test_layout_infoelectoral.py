"""
Tests del layout de Infoelectoral.

Van en dos bloques, y la diferencia importa:

  - Los que NO necesitan datos comprueban el parseador contra especificaciones
    sinteticas, incluidas varias ROTAS a proposito. Un parseador de layouts
    validado solo con el caso bueno esta sin validar: los layouts mal leidos no
    fallan, devuelven numeros creibles.

  - Los que SI necesitan datos son los que de verdad cierran el asunto: cogen los
    .dat reales del zip y comprueban que el esquema leido del .doc encaja al byte
    con ellos. Se saltan si no hay descarga local (data/external/ esta fuera de
    git), y el motivo del salto dice como conseguirla.
"""

import zipfile
from pathlib import Path

import pytest

from layout_infoelectoral import (
    Campo,
    EspecificacionIlegible,
    esquema_de_zip,
    parsear_especificacion,
)
from lector_doc import DocIlegible, texto_de_doc

RAIZ = Path(__file__).resolve().parents[2]
RUTA_ZIP = RAIZ / "data" / "external" / "infoelectoral" / "02201911_MESA.zip"

necesita_descarga = pytest.mark.skipif(
    not RUTA_ZIP.exists(),
    reason="falta %s -- bajalo con: python src/v2/descarga_infoelectoral.py 2019 11"
    % RUTA_ZIP.relative_to(RAIZ),
)


# --------------------------------------------------------------------------
# Bloque 1: el parseador, con especificaciones fabricadas a mano
# --------------------------------------------------------------------------

def _tabla(patron, titulo, filas_campos):
    """Fabrica el texto de una tabla de layout tal como sale del .doc."""
    filas = [
        [patron],
        [titulo],
        ["Posiciones", "Datos"],
        ["Inicio", "Fin", "Tipo", "Long.", "Descripción"],
    ]
    filas += [[str(x) for x in f] for f in filas_campos]
    filas += [["OBSERVACIONES:\nlo que sea"]]
    return "\x07\x07".join("\x07".join(f) for f in filas)


BUENA = _tabla(
    "03xxaamm.DAT",
    "3.- Fichero de CANDIDATURAS.",
    [
        (1, 2, "Num.", 2, "Tipo de elección."),
        (3, 8, "Alf.", 6, "Siglas."),
    ],
)


def test_una_tabla_minima_se_parsea_entera():
    esq = parsear_especificacion(BUENA)
    assert set(esq) == {"03"}
    fichero = esq["03"]
    assert fichero.patron == "03xxaamm.DAT"
    assert fichero.titulo == "Fichero de CANDIDATURAS."
    assert fichero.longitud_registro == 8
    assert fichero.campos[1] == Campo(3, 8, "Alf.", 6, "Siglas.")


def test_la_rebanada_trocea_el_registro_donde_toca():
    esq = parsear_especificacion(BUENA)
    registro = "02VOX   "
    campo_siglas = esq["03"].campo("Siglas")
    assert registro[campo_siglas.rebanada] == "VOX   "


def test_nombre_de_fichero_se_construye_desde_el_codigo():
    esq = parsear_especificacion(BUENA)
    assert esq["03"].nombre_fichero("02", 2019, 11) == "03021911.DAT"


def test_un_hueco_entre_campos_revienta():
    """El fallo mas caro: un byte sin declarar corre todo lo que viene detras."""
    rota = _tabla(
        "03xxaamm.DAT",
        "3.- Fichero de CANDIDATURAS.",
        [(1, 2, "Num.", 2, "Tipo."), (4, 9, "Alf.", 6, "Siglas.")],
    )
    with pytest.raises(EspecificacionIlegible, match="empezase en 3 y empieza en 4"):
        parsear_especificacion(rota)


def test_campos_solapados_revientan():
    rota = _tabla(
        "03xxaamm.DAT",
        "3.- Fichero de CANDIDATURAS.",
        [(1, 2, "Num.", 2, "Tipo."), (2, 7, "Alf.", 6, "Siglas.")],
    )
    with pytest.raises(EspecificacionIlegible):
        parsear_especificacion(rota)


def test_longitud_que_no_cuadra_con_inicio_y_fin_revienta():
    rota = _tabla(
        "03xxaamm.DAT",
        "3.- Fichero de CANDIDATURAS.",
        [(1, 2, "Num.", 2, "Tipo."), (3, 8, "Alf.", 5, "Siglas.")],
    )
    with pytest.raises(EspecificacionIlegible, match="longitud 5"):
        parsear_especificacion(rota)


def test_un_tipo_desconocido_revienta_en_vez_de_colarse():
    rota = _tabla(
        "03xxaamm.DAT",
        "3.- Fichero de CANDIDATURAS.",
        [(1, 2, "Bin.", 2, "Tipo.")],
    )
    with pytest.raises(EspecificacionIlegible, match="Bin."):
        parsear_especificacion(rota)


def test_un_texto_sin_tablas_no_devuelve_un_esquema_vacio():
    with pytest.raises(EspecificacionIlegible):
        parsear_especificacion("un documento cualquiera sin layout ninguno")


def test_un_fichero_que_no_es_doc_no_se_lee_a_medias():
    with pytest.raises(DocIlegible):
        texto_de_doc(b"PK\x03\x04esto es un zip, no un doc")


# --------------------------------------------------------------------------
# Bloque 2: el esquema contra los ficheros reales
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def esquema():
    return esquema_de_zip(RUTA_ZIP)


@pytest.fixture(scope="module")
def zip_mesa():
    with zipfile.ZipFile(RUTA_ZIP) as z:
        yield z


@necesita_descarga
def test_la_especificacion_declara_los_doce_ficheros(esquema):
    assert sorted(esquema) == ["%02d" % i for i in range(1, 13)]


@necesita_descarga
def test_los_tres_ambitos_traen_la_misma_especificacion():
    """TOTA, MUNI y MESA solo se diferencian en que ficheros de datos incluyen."""
    otros = sorted(RUTA_ZIP.parent.glob("02201911_*.zip"))
    if len(otros) < 2:
        pytest.skip("solo hay un ambito descargado")
    esquemas = [esquema_de_zip(r) for r in otros]
    for otro in esquemas[1:]:
        assert otro == esquemas[0]


@necesita_descarga
def test_cada_registro_real_mide_lo_que_dice_la_especificacion(esquema, zip_mesa):
    """El control que cierra el asunto: especificacion contra fichero, al byte."""
    comprobados = 0
    for nombre in sorted(n for n in zip_mesa.namelist() if n.upper().endswith(".DAT")):
        fichero = esquema[nombre[:2]]
        lineas = zip_mesa.read(nombre).split(b"\n")
        assert lineas[-1] == b"", "%s no termina en delimitador" % nombre
        largos = {len(l) for l in lineas[:-1]}
        assert largos == {fichero.longitud_registro}, (
            "%s: registros de %s bytes, la especificacion dice %d"
            % (nombre, sorted(largos), fichero.longitud_registro)
        )
        comprobados += 1
    assert comprobados == 10, "el zip MESA de un Congreso trae 10 ficheros de datos"


@necesita_descarga
def test_el_delimitador_es_LF_pese_a_lo_que_dice_la_especificacion(zip_mesa):
    """La especificacion dice CR+LF en su primer parrafo. Los ficheros llevan LF.

    Este test esta escrito al reves a proposito: fija la realidad medida, no la
    frase del documento. Si una convocatoria futura publicase de verdad con CR+LF,
    este test se pone rojo -- que es justo lo que hace falta, porque descontar dos
    bytes donde hay uno desplaza todos los campos a partir del segundo registro.
    """
    for nombre in (n for n in zip_mesa.namelist() if n.upper().endswith(".DAT")):
        assert b"\r" not in zip_mesa.read(nombre), "%s trae CR" % nombre


@necesita_descarga
def test_los_campos_numericos_traen_digitos_en_los_ficheros_reales(esquema, zip_mesa):
    for nombre in sorted(n for n in zip_mesa.namelist() if n.upper().endswith(".DAT")):
        fichero = esquema[nombre[:2]]
        lineas = zip_mesa.read(nombre).split(b"\n")[:-1]
        for linea in lineas[:2000]:
            registro = linea.decode("cp1252")
            for campo in fichero.campos:
                if campo.es_numerico:
                    trozo = registro[campo.rebanada]
                    assert trozo.isdigit(), (
                        "%s: el campo %d-%d (%s) trae %r"
                        % (nombre, campo.inicio, campo.fin, campo.descripcion, trozo)
                    )


@necesita_descarga
def test_el_fichero_de_control_coincide_con_lo_que_trae_el_zip(esquema, zip_mesa):
    """El propio 01 declara que ficheros se adjuntan. Se contrasta con el zip.

    Es la comprobacion cruzada mas barata que hay: usa el esquema para leer datos
    reales y el resultado se puede verificar sin salir del zip.
    """
    control = esquema["01"]
    registro = zip_mesa.read("01021911.DAT").split(b"\n")[0].decode("cp1252")
    presentes = {n.upper() for n in zip_mesa.namelist()}
    declarados = 0
    for campo in control.campos:
        if "se adjunta" not in campo.descripcion:
            continue
        esperado = registro[campo.rebanada] == "1"
        # La descripcion nombra el fichero: "...el fichero 09xxaamm.dat)".
        patron = campo.descripcion.rsplit(" ", 1)[-1].rstrip(").").upper()
        nombre = patron.replace("XXAAMM", "021911").replace("AAMM", "1911")
        assert (nombre in presentes) == esperado, (
            "el control dice %s para %s y el zip dice lo contrario" % (esperado, nombre)
        )
        declarados += 1
    assert declarados == 16
