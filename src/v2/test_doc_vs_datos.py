"""
El documento de diseno y el dato tienen que decir el mismo numero.

Por que existe este fichero.

`docs/v2_alcance.md` publicaba "98,42 % de secciones intactas, 572 rompen la
comparacion". El codigo producia 97,77 % y 810. Ninguna de las dos cifras estaba
mal calculada: el detector aprendio DESPUES a ver fusiones -- una seccion que
absorbe a otra tampoco es el mismo trozo de mapa -- y encontro 238 mas. El
codigo las contaba y el documento no, porque un numero escrito a mano en prosa no
se entera de que el codigo ha mejorado.

Estuvo semanas asi, y no habia forma de notarlo: los dos ficheros eran
coherentes consigo mismos.

Lo que se pin_a aqui no es la cifra concreta -- esa cambiara cuando cambien los
datos o el umbral -- sino que las dos fuentes coincidan. Si vuelven a separarse,
esto falla y dice cual es cual.
"""
import json
import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
JSON_SUPERVIVENCIA = RAIZ / "data" / "processed" / "v2" / "supervivencia_secciones.json"
DOC = RAIZ / "docs" / "v2_alcance.md"

# El umbral que el proyecto usa para decidir si una seccion se partio. Vive en
# supervivencia_secciones.py; aqui se nombra para que el test diga contra que
# columna del JSON compara, no para redefinirlo.
UMBRAL = "0.3"

necesita_el_json = pytest.mark.skipif(
    not JSON_SUPERVIVENCIA.exists(),
    reason="falta supervivencia_secciones.json -- generalo con: "
    "python src/v2/supervivencia_secciones.py",
)


def _cifras_del_dato():
    d = json.loads(JSON_SUPERVIVENCIA.read_text(encoding="utf-8"))
    real = d["REAL"]
    origen = real["secciones_origen"]
    umbral = real["umbrales"][UMBRAL]
    intactas = umbral["identidad_real"]
    return {
        "origen": origen,
        "intactas": intactas,
        "rompen": origen - intactas,
        "pct_intactas": 100.0 * intactas / origen,
        "ocultas": umbral["ocultas"],
        "fusiones": umbral["fusiones"],
    }


def _como_lo_escribe_el_doc(n):
    """36302 -> "36.302". El documento usa el punto como separador de miles."""
    return "{:,}".format(int(n)).replace(",", ".")


def _pct_como_lo_escribe_el_doc(x):
    """97.77 -> "97,77". Coma decimal, dos cifras."""
    return ("%.2f" % x).replace(".", ",")


@necesita_el_json
def test_el_doc_publica_las_secciones_intactas_que_calcula_el_codigo():
    c = _cifras_del_dato()
    esperado = _como_lo_escribe_el_doc(c["intactas"])
    assert esperado in DOC.read_text(encoding="utf-8"), (
        "el codigo calcula %s secciones intactas y el documento no lo dice en ningun sitio.\n"
        "Si el numero ha cambiado, actualiza docs/v2_alcance.md: la cifra vive en dos sitios y "
        "solo uno de los dos se entera de que el detector ha mejorado." % esperado
    )


@necesita_el_json
def test_el_doc_publica_cuantas_rompen_la_comparacion():
    c = _cifras_del_dato()
    esperado = _como_lo_escribe_el_doc(c["rompen"])
    texto = DOC.read_text(encoding="utf-8")
    assert esperado in texto, (
        "rompen la comparacion %s secciones y el documento no las menciona.\n"
        "Aviso: %s = particiones ocultas (%d) + fusiones (%d) + muertas + las que solo encogen. "
        "La version anterior del documento decia 572 porque no contaba las fusiones."
        % (esperado, esperado, c["ocultas"], c["fusiones"])
    )


@necesita_el_json
def test_el_doc_publica_el_porcentaje_que_calcula_el_codigo():
    c = _cifras_del_dato()
    esperado = _pct_como_lo_escribe_el_doc(c["pct_intactas"])
    assert esperado in DOC.read_text(encoding="utf-8"), (
        "el codigo da %s %% de secciones intactas y el documento no lo dice." % esperado
    )


@necesita_el_json
def test_el_doc_no_publica_la_cifra_vieja_como_si_fuera_actual():
    """La cifra retirada puede aparecer -- pero solo contada como historia.

    El documento explica que antes decia 98,42 % y por que cambio. Eso es
    correcto y hay que poder escribirlo. Lo que no puede es aparecer suelta, en
    una tabla o en una frase, como si siguiera siendo el resultado.
    """
    texto = DOC.read_text(encoding="utf-8")
    lineas_con_la_vieja = [
        linea for linea in texto.splitlines() if "98,42" in linea or "35.730" in linea
    ]
    for linea in lineas_con_la_vieja:
        assert re.search(r"dec[ií]a|antes|hasta el|hist[oó]ric", linea, re.IGNORECASE), (
            "la cifra retirada aparece sin decir que es historica:\n    %s" % linea.strip()
        )


@necesita_el_json
def test_las_fusiones_no_se_pueden_volver_a_perder():
    """El fallo concreto: el documento contaba particiones y no fusiones.

    Las dos rompen la comparacion por el mismo motivo -- deja de ser el mismo
    trozo de mapa -- y el documento solo nombraba una.
    """
    c = _cifras_del_dato()
    assert c["fusiones"] > 0, "el JSON no trae fusiones: ¿se ha revertido el detector?"
    texto = DOC.read_text(encoding="utf-8")
    assert "fusion" in texto.lower() or "fusión" in texto.lower(), (
        "el documento no menciona las fusiones, y son %d de las %d que rompen la comparacion"
        % (c["fusiones"], c["rompen"])
    )
