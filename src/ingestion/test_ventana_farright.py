"""Reproduce y cierra BUG-LA-VENTANA-TEMPORAL-DE.

`load_populist()` lee `farright_start`/`farright_end` del PopuList y `calculate_nationalist_vote()`
los tira: construye `far_right_ids` como un set sin año y por tanto cuenta a un partido como
far-right en TODOS los años, incluidos los que PopuList declara fuera de la etiqueta. Caso real
medido sobre data/raw: Fidesz (partyfacts_id 1691, farright_start=2010) entraba como nacionalista
en las húngaras de 2002 y 2006.

Estos tests no tocan data/raw (read-only, y no existe en este worktree): construyen a mano los
DataFrames con el mismo esquema que devuelven `load_euned`/`load_poppa`/`load_populist`.
"""
import math

import pandas as pd

from load_euned import calculate_nationalist_vote


def _poppa(partyfacts_id, nativism):
    return pd.DataFrame([{
        'partyfacts_id': partyfacts_id,
        'party_name_english': 'Partido de prueba',
        'country': 'HU',
        'nativism': nativism,
        'populism_mean': 5.0,
    }])


def _populist(partyfacts_id, farright_start, farright_end):
    return pd.DataFrame([{
        'partyfacts_id': partyfacts_id,
        'party_name_english': 'Partido de prueba',
        'farright': 1,
        'farright_start': farright_start,
        'farright_end': farright_end,
    }])


def _euned(partyfacts_id, year, vote_share=42.0):
    return pd.DataFrame([{
        'nuts2': 'HU10',
        'regionname': 'Región de prueba',
        'country_code': 'HU',
        'year': year,
        'partyfacts_id': partyfacts_id,
        'party_abbreviation': 'TEST',
        'vote_share': vote_share,
    }])


def test_anio_anterior_al_inicio_se_excluye():
    """Fidesz-como-caso: farright_start=2010, elección de 2006 -> no cuenta como nacionalista."""
    df_euned = _euned(partyfacts_id=1691, year=2006)
    df_poppa = _poppa(partyfacts_id=1691, nativism=9.0)
    df_populist = _populist(partyfacts_id=1691, farright_start=2010, farright_end=math.nan)

    resultado = calculate_nationalist_vote(df_euned, df_poppa, df_populist)

    # BUG-481-DE-1031-REGION: la región-año ya no desaparece, sale con cero declarado — lo
    # que se comprueba aquí es que el voto NO cuenta como nacionalista, no que falte la fila.
    assert len(resultado) == 1
    assert resultado.iloc[0]['nationalist_vote_share'] == 0.0, (
        "el partido tenía nativism>=umbral y está en PopuList, pero la elección de 2006 es "
        "ANTERIOR a farright_start=2010: no debería contar como nacionalista"
    )


def test_anio_dentro_de_la_ventana_se_incluye():
    """El mismo partido, en un año DENTRO de su ventana declarada, sí cuenta."""
    df_euned = _euned(partyfacts_id=1691, year=2014)
    df_poppa = _poppa(partyfacts_id=1691, nativism=9.0)
    df_populist = _populist(partyfacts_id=1691, farright_start=2010, farright_end=math.nan)

    resultado = calculate_nationalist_vote(df_euned, df_poppa, df_populist)

    assert len(resultado) == 1
    assert resultado.iloc[0]['nationalist_vote_share'] == 42.0


def test_posterior_al_fin_de_la_ventana_se_excluye():
    """farright_end acota también el lado tardío: un año posterior al fin queda fuera."""
    df_euned = _euned(partyfacts_id=1976, year=2018)
    df_poppa = _poppa(partyfacts_id=1976, nativism=8.0)
    df_populist = _populist(partyfacts_id=1976, farright_start=2013, farright_end=2015)

    resultado = calculate_nationalist_vote(df_euned, df_poppa, df_populist)

    # BUG-481-DE-1031-REGION: cero declarado, no fila ausente (ver test anterior).
    assert len(resultado) == 1
    assert resultado.iloc[0]['nationalist_vote_share'] == 0.0


def test_ventana_sin_limites_declarados_no_excluye_nada():
    """farright_start/end en NaN (PopuList sin fecha declarada) significa "sin límite", no
    "excluir siempre": el partido debe seguir contando en cualquier año si cumple lo demás."""
    df_euned = _euned(partyfacts_id=42, year=1995)
    df_poppa = _poppa(partyfacts_id=42, nativism=8.0)
    df_populist = _populist(partyfacts_id=42, farright_start=math.nan, farright_end=math.nan)

    resultado = calculate_nationalist_vote(df_euned, df_poppa, df_populist)

    assert len(resultado) == 1
