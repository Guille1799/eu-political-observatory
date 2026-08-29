"""
[HISTORICO - v1] Ingesta de la base electoral europea. NO esta en el camino de la
linea de trabajo actual (v2, espanola y subnacional -- ver docs/v2_alcance.md).

BUG CONOCIDO Y NO ARREGLADO: la regla de clasificacion `nativism>=7` AND `far-right`
solo ve el 10% del voto y marca 38 partidos. No es una regla conservadora: convierte
"no medido" en "no nacionalista", que es un error con signo. Se deja documentado en
vez de arreglado porque este codigo ya no esta en el camino; si alguna vez vuelve a
usarse, esto es lo primero que hay que tocar.
"""

import pandas as pd
import psycopg2
import os
import io
from dotenv import load_dotenv

# El repo no tiene estructura de paquete y estos scripts se ejecutan como
# `python src/ingestion/load_euned.py` desde la raíz — el import del vecino se resuelve
# por el directorio del propio script, que Python pone en sys.path.
from parameters import NATIVISM_THRESHOLD

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

COUNTRIES = ['ES', 'DE', 'FR', 'IT', 'PL', 'HU', 'SE']


def load_euned(filepath):
    """
    Lee el CSV de EU-NED y calcula el porcentaje de voto
    por partido en cada región y año.
    """
    df = pd.read_csv(filepath)
    df = df[df['country_code'].isin(COUNTRIES)]
    df = df[df['type'] == 'Parliament']
    df = df[df['nutslevel'] == 2]
    df['vote_share'] = df['partyvote'] / df['validvote'] * 100
    df = df[['nuts2', 'regionname', 'country_code', 'year',
             'partyfacts_id', 'party_abbreviation', 'vote_share']]
    df = df.dropna(subset=['partyfacts_id'])
    df['partyfacts_id'] = df['partyfacts_id'].astype(int)
    return df


def load_poppa(filepath):
    """
    Lee el CSV de POPPA y extrae el score de nativismo
    por partido para identificar partidos nacionalistas.
    """
    df = pd.read_csv(filepath)
    df = df[['partyfacts_id', 'party_name_english', 'country',
             'nativism', 'populism_mean']]
    df = df.dropna(subset=['partyfacts_id'])
    df['partyfacts_id'] = df['partyfacts_id'].astype(int)
    df = df.groupby('partyfacts_id').agg({
        'party_name_english': 'first',
        'country': 'first',
        'nativism': 'mean',
        'populism_mean': 'mean'
    }).reset_index()
    return df


def load_populist(filepath):
    """
    Lee el CSV del PopuList y extrae los partidos clasificados
    como far-right para validación cruzada con POPPA.
    """
    df = pd.read_csv(filepath, sep=';')
    df.columns = df.columns.str.replace('\ufeff', '')
    df = df[df['farright'] == 1]
    df = df[['partyfacts_id', 'party_name_english', 'farright',
             'farright_start', 'farright_end']]
    df = df.dropna(subset=['partyfacts_id'])
    df['partyfacts_id'] = df['partyfacts_id'].astype(int)
    return df


def calculate_nationalist_vote(df_euned, df_poppa, df_populist,
                               nativism_threshold=NATIVISM_THRESHOLD):
    """
    Cruza EU-NED con POPPA y PopuList para calcular el índice
    ponderado de voto nacionalista por región y año.

    Un partido es nacionalista si cumple AMBAS condiciones:
    1. Score de nativismo >= NATIVISM_THRESHOLD en POPPA (procedencia: parameters.py)
    2. Clasificado como far-right en PopuList

    El índice pondera el voto por el score de nativismo
    para reflejar la intensidad del nacionalismo.
    """
    # Cruzar EU-NED con POPPA via partyfacts_id
    df = df_euned.merge(df_poppa, on='partyfacts_id', how='left')

    # Cruzar con la ventana temporal far-right de PopuList — un partido solo cuenta como
    # far-right en los años que PopuList declara (farright_start/farright_end); NaN en un
    # extremo significa "sin límite declarado" en ese lado.
    df = df.merge(
        df_populist[['partyfacts_id', 'farright_start', 'farright_end']],
        on='partyfacts_id', how='left'
    )

    # Lista de partidos far-right del PopuList
    far_right_ids = set(df_populist['partyfacts_id'].tolist())

    en_ventana = (
        (df['farright_start'].isna() | (df['year'] >= df['farright_start'])) &
        (df['farright_end'].isna() | (df['year'] <= df['farright_end']))
    )

    es_nacionalista = (
        (df['nativism'] >= nativism_threshold) &
        (df['partyfacts_id'].isin(far_right_ids)) &
        en_ventana
    )

    # Calcular índice ponderado — voto × nativismo / 10
    df['weighted_vote'] = df['vote_share'] * df['nativism'] / 10

    # Un partido tiene VEREDICTO cuando aparece en POPPA (nativism no nulo): solo entonces
    # se pudo evaluar la primera condición. Si no aparece, "no cumple" y "no se midió" son
    # indistinguibles si no se declaran aparte.
    df['tiene_veredicto'] = df['nativism'].notna()

    grupo = ['nuts2', 'regionname', 'country_code', 'year']

    # La cobertura corre sobre TODA la entrada de EU-NED, no solo sobre los partidos que
    # acaban siendo nacionalistas — así una región-año sin ningún nacionalista sigue
    # emitiendo fila, con su cero declarado y su cobertura (en vez de desaparecer).
    cobertura = df.groupby(grupo).agg(
        partidos_totales=('partyfacts_id', 'count'),
        partidos_con_veredicto=('tiene_veredicto', 'sum'),
    ).reset_index()

    df_nationalist = df[es_nacionalista]
    votos = df_nationalist.groupby(grupo).agg(
        nationalist_vote_share=('vote_share', 'sum'),
        nationalist_weighted_index=('weighted_vote', 'sum'),
    ).reset_index()

    df_result = cobertura.merge(votos, on=grupo, how='left')
    df_result['nationalist_vote_share'] = df_result['nationalist_vote_share'].fillna(0.0)
    df_result['nationalist_weighted_index'] = df_result['nationalist_weighted_index'].fillna(0.0)

    return df_result


def save_to_postgres(df, table_name):
    """
    Guarda un DataFrame en PostgreSQL usando copy_expert.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Eliminar tabla si existe
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Crear tabla — incluye la cobertura (cuántos partidos de la región-año tenían
    # veredicto) para que un cero declarado se distinga de "sin datos" también en Postgres.
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            nuts2_id VARCHAR(10),
            region_name VARCHAR(100),
            country_code VARCHAR(5),
            year INTEGER,
            partidos_totales INTEGER,
            partidos_con_veredicto INTEGER,
            nationalist_vote_share FLOAT,
            nationalist_weighted_index FLOAT
        )
    """)

    columnas = ['nuts2', 'regionname', 'country_code', 'year',
                'partidos_totales', 'partidos_con_veredicto',
                'nationalist_vote_share', 'nationalist_weighted_index']
    buffer = io.StringIO()
    df[columnas].to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    cursor.copy_expert(f"""
        COPY {table_name} (nuts2_id, region_name, country_code, year,
        partidos_totales, partidos_con_veredicto,
        nationalist_vote_share, nationalist_weighted_index)
        FROM STDIN WITH CSV
    """, buffer)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✓ Datos guardados en tabla '{table_name}'")


if __name__ == "__main__":

    euned_file = "data/raw/eu_ned_joint_nuts2.csv"
    poppa_file = "data/raw/poppa_integrated_v2.csv"
    populist_file = "data/raw/The PopuList 3.0.csv"

    print("Cargando datos...")
    df_euned = load_euned(euned_file)
    df_poppa = load_poppa(poppa_file)
    df_populist = load_populist(populist_file)

    print("Calculando índice de voto nacionalista...")
    df_nationalist = calculate_nationalist_vote(df_euned, df_poppa, df_populist)

    print(f"Región-año emitidas (con cero declarado o veredicto): {len(df_nationalist)}")
    print(df_nationalist.head(10))

    print("Guardando en PostgreSQL...")
    save_to_postgres(df_nationalist, 'nationalist_vote')

    print("✓ Proceso completado")