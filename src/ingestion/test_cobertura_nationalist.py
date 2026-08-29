"""Reproduce y cierra BUG-481-DE-1031-REGION.

`calculate_nationalist_vote()` agrupaba SOLO sobre las filas que ya habían pasado el filtro
de "es nacionalista", así que una región-año donde de verdad ningún partido cumplía la doble
condición y una región-año cuyos partidos ni siquiera estaban en POPPA/PopuList producían
exactamente el mismo resultado: la fila no aparecía. Medido sobre data/raw: de 1031 pares
(nuts2, year) en la entrada, solo 550 salían en el resultado — 481 desaparecían sin dejar
rastro de si el cero era medido o si nadie tenía veredicto.

Estos tests no tocan data/raw (read-only, y no existe en este worktree): construyen a mano
los DataFrames con el mismo esquema que devuelven `load_euned`/`load_poppa`/`load_populist`.
"""
import math

import pandas as pd

from load_euned import calculate_nationalist_vote


def _euned(filas):
    return pd.DataFrame([{
        'nuts2': 'ES30',
        'regionname': 'Región de prueba',
        'country_code': 'ES',
        'year': 2015,
        'party_abbreviation': 'TEST',
        **fila,
    } for fila in filas])


def test_region_sin_nacionalistas_sale_con_cero():
    """Un partido evaluado (está en POPPA y en PopuList) pero por debajo del umbral: la
    región-año debe seguir saliendo, con voto nacionalista CERO declarado — no ausente."""
    df_euned = _euned([{'partyfacts_id': 1, 'vote_share': 55.0}])
    df_poppa = pd.DataFrame([{
        'partyfacts_id': 1, 'party_name_english': 'Partido de prueba', 'country': 'ES',
        'nativism': 2.0, 'populism_mean': 3.0,
    }])
    df_populist = pd.DataFrame([{
        'partyfacts_id': 1, 'party_name_english': 'Partido de prueba', 'farright': 1,
        'farright_start': math.nan, 'farright_end': math.nan,
    }])

    resultado = calculate_nationalist_vote(df_euned, df_poppa, df_populist)

    assert len(resultado) == 1, "la región-año tiene que seguir saliendo, no desaparecer"
    fila = resultado.iloc[0]
    assert fila['nationalist_vote_share'] == 0.0
    assert fila['nationalist_weighted_index'] == 0.0
    assert fila['partidos_totales'] == 1
    assert fila['partidos_con_veredicto'] == 1, (
        "el partido SÍ estaba en POPPA: tuvo veredicto, solo que no cumplía el umbral"
    )


def test_region_sin_datos_de_poppa_ni_populist_se_distingue_del_cero_medido():
    """Un partido que no aparece ni en POPPA ni en PopuList: la región-año también sale, pero
    con partidos_con_veredicto=0, para no confundirla con la que sí se evaluó y dio cero."""
    df_euned = _euned([{'partyfacts_id': 99, 'vote_share': 30.0}])
    df_poppa = pd.DataFrame(columns=['partyfacts_id', 'party_name_english', 'country',
                                      'nativism', 'populism_mean'])
    df_populist = pd.DataFrame(columns=['partyfacts_id', 'party_name_english', 'farright',
                                         'farright_start', 'farright_end'])

    resultado = calculate_nationalist_vote(df_euned, df_poppa, df_populist)

    assert len(resultado) == 1
    fila = resultado.iloc[0]
    assert fila['nationalist_vote_share'] == 0.0
    assert fila['partidos_totales'] == 1
    assert fila['partidos_con_veredicto'] == 0, (
        "sin match en POPPA no hubo veredicto: distinto de un cero medido"
    )


def test_region_con_un_nacionalista_y_otro_sin_veredicto_suma_solo_el_que_cumple():
    """Región con dos partidos: uno nacionalista claro y otro sin match en POPPA. El resultado
    debe sumar solo el voto del que cumple, pero contar la cobertura de los dos."""
    df_euned = _euned([
        {'partyfacts_id': 1, 'vote_share': 40.0},
        {'partyfacts_id': 2, 'vote_share': 20.0},
    ])
    df_poppa = pd.DataFrame([{
        'partyfacts_id': 1, 'party_name_english': 'Nacionalista', 'country': 'ES',
        'nativism': 9.0, 'populism_mean': 5.0,
    }])
    df_populist = pd.DataFrame([{
        'partyfacts_id': 1, 'party_name_english': 'Nacionalista', 'farright': 1,
        'farright_start': math.nan, 'farright_end': math.nan,
    }])

    resultado = calculate_nationalist_vote(df_euned, df_poppa, df_populist)

    assert len(resultado) == 1
    fila = resultado.iloc[0]
    assert fila['nationalist_vote_share'] == 40.0
    assert fila['partidos_totales'] == 2
    assert fila['partidos_con_veredicto'] == 1
