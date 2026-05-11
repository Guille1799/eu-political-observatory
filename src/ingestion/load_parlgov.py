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

COUNTRIES = ['DEU', 'ESP', 'FRA', 'ITA', 'POL', 'HUN', 'SWE']
YEAR_START = 2008
YEAR_END = 2024


def load_parlgov(election_filepath, crosswalk_filepath):
    """
    Lee view_election de ParlGov y añade partyfacts_id
    via la tabla de correspondencia crosswalk.
    """
    df = pd.read_csv(election_filepath)
    df = df[df['election_type'] == 'parliament']
    df = df[df['country_name_short'].isin(COUNTRIES)]
    df['year'] = pd.to_datetime(df['election_date']).dt.year
    df = df[(df['year'] >= YEAR_START) & (df['year'] <= YEAR_END)]
    df = df.dropna(subset=['vote_share'])
    crosswalk = pd.read_csv(crosswalk_filepath)
    df = df.merge(crosswalk, left_on='party_id', right_on='parlgov_id', how='left')
    df = df[['country_name_short', 'election_date', 'year',
             'party_name_short', 'party_id', 'partyfacts_id', 'vote_share']]
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


def calculate_nationalist_vote_parlgov(df_parlgov, df_poppa, df_populist, nativism_threshold=7.0):
    """
    Cruza ParlGov con POPPA y PopuList para calcular el índice
    ponderado de voto nacionalista por país y año.
    """
    df = df_parlgov.merge(df_poppa, on='partyfacts_id', how='left')
    far_right_ids = set(df_populist['partyfacts_id'].tolist())
    df_nationalist = df[
        (df['nativism'] >= nativism_threshold) &
        (df['partyfacts_id'].isin(far_right_ids))
    ].copy()
    df_nationalist['weighted_vote'] = df_nationalist['vote_share'] * df_nationalist['nativism'] / 10
    df_result = df_nationalist.groupby(
        ['country_name_short', 'year']
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
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute(f"""
        CREATE TABLE {table_name} (
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
        COPY {table_name} (country_code, year,
        nationalist_vote_share, nationalist_weighted_index)
        FROM STDIN WITH CSV
    """, buffer)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✓ Datos guardados en tabla '{table_name}'")


if __name__ == "__main__":

    parlgov_file = "data/raw/view_election.csv"
    crosswalk_file = "data/raw/partyfacts-parlgov-ids.csv"
    poppa_file = "data/raw/poppa_integrated_v2.csv"
    populist_file = "data/raw/The PopuList 3.0.csv"

    print("Cargando datos...")
    df_parlgov = load_parlgov(parlgov_file, crosswalk_file)
    df_poppa = load_poppa(poppa_file)
    df_populist = load_populist(populist_file)

    print("Calculando índice de voto nacionalista...")
    df_nationalist = calculate_nationalist_vote_parlgov(df_parlgov, df_poppa, df_populist)

    print(f"Registros detectados: {len(df_nationalist)}")
    print(df_nationalist)

    print("Guardando en PostgreSQL...")
    save_to_postgres(df_nationalist, 'nationalist_vote_national')

    print("✓ Proceso completado")