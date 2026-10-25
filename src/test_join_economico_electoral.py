#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests NEGATIVOS de `join_economico_electoral.py`.

Motivo de existir: una aserción que nunca ha fallado no está comprobada, está
supuesta. Aquí se corrompe el dato a propósito, caso por caso, y se exige que
el pipeline se pare. La primera versión de este fichero descubrió que dos
aserciones eran decorativas (la de conservación de votos cuadraba en falso
porque `sum()` ignora los NaN a los dos lados).

BUG-PYTEST-SRC-SALE-VERDE (2026-08-22): el fichero se llamaba `test_*.py` (pytest
lo recoge) pero no exponía ninguna función `test_*` -- solo una `class Runner` y
un `main()` -- así que `pytest src/` lo importaba, no encontraba nada, y lo daba
por bueno en silencio. Reescrito como funciones `test_*` reales.

No usa `data/raw/` (no existe en el worktree de Ralph): `elec2` y `panel` son
fixtures sintéticas con la misma forma que producen `load_euned()` y
`build_ardeco_panel()` -- mismas claves, mismas columnas, aritmética de votos
válida -- así que ejercen las mismas aserciones duras sin depender del dato real.

Uso:  python src/test_join_economico_electoral.py     (sale 1 si algo falla)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import join_economico_electoral as J  # noqa: E402


def _synthetic_elec2() -> pd.DataFrame:
    """Forma de `load_euned()`: dos regiones NUTS2 (ES11, ES12) bajo el mismo
    NUTS1 (ES1), dos partidos por región, aritmética de votos válida."""
    rows = [
        # country_code, country_nuts, nuts2_id, nuts1_id, year, type,
        # party_abbreviation, party_english, partyfacts_id,
        # partyvote, validvote, totalvote, electorate
        ("ES", "ES", "ES11", "ES1", 2019, "Parliament", "P1", "Party One", 1,
         1000, 5000, 5200, 8000),
        ("ES", "ES", "ES11", "ES1", 2019, "Parliament", "P2", "Party Two", 2,
         4000, 5000, 5200, 8000),
        ("ES", "ES", "ES12", "ES1", 2019, "Parliament", "P1", "Party One", 1,
         2000, 6000, 6300, 9000),
        ("ES", "ES", "ES12", "ES1", 2019, "Parliament", "P2", "Party Two", 2,
         3900, 6000, 6300, 9000),
    ]
    return pd.DataFrame(rows, columns=[
        "country_code", "country_nuts", "nuts2_id", "nuts1_id", "year", "type",
        "party_abbreviation", "party_english", "partyfacts_id",
        "partyvote", "validvote", "totalvote", "electorate",
    ])


def _synthetic_panel() -> pd.DataFrame:
    """Forma de `build_ardeco_panel()`: los mismos códigos NUTS2 de
    `_synthetic_elec2()` más su NUTS1 agregado, un único año."""
    rows = [
        ("ES11", 2019, 2, 100.0),
        ("ES12", 2019, 2, 110.0),
        ("ES1", 2019, 1, 105.0),
    ]
    return pd.DataFrame(rows, columns=["region_id", "year", "nuts_level", "gdp_pps"])


@pytest.fixture(scope="module")
def elec2() -> pd.DataFrame:
    return _synthetic_elec2()


@pytest.fixture(scope="module")
def panel() -> pd.DataFrame:
    return _synthetic_panel()


# --- aritmética de votos ---
def test_partyvote_mayor_que_validvote(elec2):
    d = elec2.copy()
    i = d.index[0]
    d.loc[i, "partyvote"] = d.loc[i, "validvote"] + 1
    with pytest.raises(AssertionError):
        J.check_vote_arithmetic(d)


def test_totalvote_mayor_que_electorate(elec2):
    d = elec2.copy()
    i = d[d["electorate"].notna() & d["totalvote"].notna()].index[0]
    d.loc[i, "totalvote"] = d.loc[i, "electorate"] + 1
    with pytest.raises(AssertionError):
        J.check_vote_arithmetic(d)


def test_violacion_nueva_de_monotonicidad(elec2):
    # ES no está en la línea base conocida: una violación aquí es NUEVA y debe abortar.
    d = elec2.copy()
    i = d[(d["country_code"] == "ES") & d["totalvote"].notna()].index[0]
    d.loc[i, "validvote"] = d.loc[i, "totalvote"] + 1
    with pytest.raises(AssertionError):
        J.check_vote_arithmetic(d)


def test_violaciones_linea_base_no_abortan(elec2):
    J.check_vote_arithmetic(elec2)


# --- agregación a NUTS1 ---
def test_partyvote_con_nan_rompe_nuts1(elec2):
    d = elec2.copy()
    d.loc[d.index[0], "partyvote"] = np.nan
    with pytest.raises(AssertionError):
        J.build_nuts1(d)


def test_agregacion_nuts1_sobre_dato_real(elec2):
    J.build_nuts1(elec2)


# --- códigos y claves de EU-NED, a través de `load_euned()` ---
# Las aserciones duras viven DENTRO de `load_euned()`. Los tests anteriores recalculaban la condición en el
# propio test y llamaban a `AUDIT.hard` ellos mismos: probaban `AUDIT.hard`, no el pipeline, y seguían en verde
# aunque se borrase la aserción de producción. Aquí el CSV sintético se escribe donde `load_euned()` lo lee.
@pytest.fixture
def euned_en_disco(tmp_path, monkeypatch):
    def cargar(filas: pd.DataFrame) -> pd.DataFrame:
        csv = filas.rename(columns={"nuts2_id": "nuts2"}).drop(columns=["country_nuts", "nuts1_id"])
        for nombre in ("joint", "national"):
            csv.to_csv(tmp_path / f"{nombre}.csv", index=False)
        monkeypatch.setattr(J, "EUNED_JOINT", tmp_path / "joint.csv")
        monkeypatch.setattr(J, "EUNED_NATIONAL", tmp_path / "national.csv")
        return J.load_euned()

    return cargar


def test_load_euned_acepta_el_dato_sano(euned_en_disco, elec2):
    assert len(euned_en_disco(elec2)) == len(elec2)


def _con_la_clave_repetida(d: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([d, d.head(1)], ignore_index=True)


def _con_el_codigo(codigo: str):
    def corrompe(d: pd.DataFrame) -> pd.DataFrame:
        d = d.copy()
        d.loc[d.index[0], "nuts2_id"] = codigo
        return d

    return corrompe


@pytest.mark.parametrize(
    "corrompe, mensaje",
    [
        pytest.param(_con_la_clave_repetida, "filas duplicadas", id="clave-duplicada"),
        pytest.param(_con_el_codigo("XXXXX"), "longitud != 4", id="codigo-NUTS2-de-5-caracteres"),
        pytest.param(_con_el_codigo("ZZ11"), "prefijo de pais", id="prefijo-que-no-es-el-del-pais"),
    ],
)
def test_load_euned_se_para_con_dato_corrupto(euned_en_disco, elec2, corrompe, mensaje):
    with pytest.raises(AssertionError, match=mensaje):
        euned_en_disco(corrompe(elec2))


# --- merge ---
def test_merge_duplicaria(elec2, panel):
    n2 = panel[panel["nuts_level"] == 2]
    p = pd.concat([panel, n2.head(3)], ignore_index=True)
    with pytest.raises(pd.errors.MergeError):
        J.merge_level(elec2, p, "nuts2_id", level=2)


def test_duplicado_otro_nivel_no_contamina(elec2, panel):
    n1 = panel[panel["nuts_level"] == 1]
    p = pd.concat([panel, n1.head(3)], ignore_index=True)
    J.merge_level(elec2, p, "nuts2_id", level=2)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
