import pandas as pd
import psycopg2
import os
import io
from dotenv import load_dotenv

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


def calculate_nationalist_vote(df_euned, df_poppa, df_populist, nativism_threshold=7.0):
    """
    Cruza EU-NED con POPPA y PopuList para calcular el índice
    ponderado de voto nacionalista por región y año.

    Un partido es nacionalista si cumple AMBAS condiciones:
    1. Score de nativismo >= 7 en POPPA
    2. Clasificado como far-right en PopuList

    El índice pondera el voto por el score de nativismo
    para reflejar la intensidad del nacionalismo.
    """
    # Cruzar EU-NED con POPPA via partyfacts_id
    df = df_euned.merge(df_poppa, on='partyfacts_id', how='left')

    # Lista de partidos far-right del PopuList
    far_right_ids = set(df_populist['partyfacts_id'].tolist())

    # Filtrar partidos nacionalistas — deben cumplir AMBAS condiciones
    df_nationalist = df[
        (df['nativism'] >= nativism_threshold) &
        (df['partyfacts_id'].isin(far_right_ids))
    ].copy()

    # Calcular índice ponderado — voto × nativismo / 10
    df_nationalist['weighted_vote'] = df_nationalist['vote_share'] * df_nationalist['nativism'] / 10

    # Sumar índice ponderado por región y año
    df_result = df_nationalist.groupby(
        ['nuts2', 'regionname', 'country_code', 'year']
    ).agg(
        nationalist_vote_share=('vote_share', 'sum'),
        nationalist_weighted_index=('weighted_vote', 'sum')
    ).reset_index()

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

    # Crear tabla
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            nuts2_id VARCHAR(10),
            region_name VARCHAR(100),
            country_code VARCHAR(5),
            year INTEGER,
            nationalist_vote_share FLOAT,
            nationalist_weighted_index FLOAT
        )
    """)

    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    cursor.copy_expert(f"""
        COPY {table_name} (nuts2_id, region_name, country_code, year,
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

    print(f"Regiones con voto nacionalista detectadas: {len(df_nationalist)}")
    print(df_nationalist.head(10))

    print("Guardando en PostgreSQL...")
    save_to_postgres(df_nationalist, 'nationalist_vote')

    print("✓ Proceso completado")