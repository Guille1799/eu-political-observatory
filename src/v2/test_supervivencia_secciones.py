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

import pytest

from supervivencia_secciones import UMBRAL_PRINCIPAL, particiones_ocultas

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
