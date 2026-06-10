import pandas as pd
import psycopg2
import os
import io
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Países de interés — códigos NUTS
COUNTRIES = ['ES', 'DE', 'FR', 'IT', 'PL', 'HU', 'SE']

# Regiones a excluir — Francia de ultramar
EXCLUDE_REGIONS = ['FRY1', 'FRY2', 'FRY3', 'FRY4']

# Rango temporal
YEAR_START = 2008
YEAR_END = 2024


def load_ardeco_file(filepath, variable_name, education_level=None):
    """
    Lee un CSV de ARDECO y lo transforma al formato largo.

    filepath: ruta al archivo CSV
    variable_name: nombre de la variable (ej: 'unemployment', 'gdp', 'education')
    education_level: si es el dataset de educación, filtrar por nivel (ej: 'ED5-8')
    """
    df = pd.read_csv(filepath)

    # Filtrar solo NUTS 2
    df = df[df['LEVEL_ID'] == 2]

    # Filtrar solo nuestros 7 países
    df = df[df['TERRITORY_ID'].str[:2].isin(COUNTRIES)]

    # Excluir Francia de ultramar
    df = df[~df['TERRITORY_ID'].isin(EXCLUDE_REGIONS)]

    # Si es educación, filtrar solo el nivel universitario ED5-8
    if education_level:
        df = df[df['ISCED11'] == education_level]

    # Seleccionar solo las columnas que necesitamos
    year_columns = [str(y) for y in range(YEAR_START, YEAR_END + 1)]
    
    # Filtrar solo columnas de años que existen en el dataset
    year_columns = [y for y in year_columns if y in df.columns]
    
    df = df[['TERRITORY_ID', 'NAME_HTML'] + year_columns]

    # Convertir columnas de años a numérico
    for col in year_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Interpolación lineal para valores vacíos
    df[year_columns] = df[year_columns].interpolate(axis=1, method='linear')

    # Transformar de formato ancho a formato largo
    df = df.melt(
        id_vars=['TERRITORY_ID', 'NAME_HTML'],
        value_vars=year_columns,
        var_name='year',
        value_name=variable_name
    )

    # Limpiar nombres de columnas
    df = df.rename(columns={
        'TERRITORY_ID': 'nuts2_id',
        'NAME_HTML': 'region_name'
    })

    # Convertir año a número entero
    df['year'] = df['year'].astype(int)

    return df


def save_to_postgres(df, table_name):
    """
    Guarda un DataFrame en PostgreSQL usando copy_expert.
    Mucho más rápido que insertar fila por fila.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Eliminar tabla si existe para evitar duplicados
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Crear tabla limpia
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            nuts2_id VARCHAR(10),
            region_name VARCHAR(100),
            year INTEGER,
            value FLOAT
        )
    """)

    # Convertir DataFrame a CSV en memoria
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    # Insertar todo de golpe
    cursor.copy_expert(f"""
        COPY {table_name} (nuts2_id, region_name, year, value)
        FROM STDIN WITH CSV
    """, buffer)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✓ Datos guardados en tabla '{table_name}'")


if __name__ == "__main__":

    # Rutas a los archivos de ARDECO
    unemployment_file = "data/raw/ARDECO-RPUCNP.versions_2024-unit_PC-level_id_2.table.csv"
    gdp_file = "data/raw/_ARDECO-SUVGDP.versions_2024-unit_EUR,PPS_EU27_2020-level_id_0,1,2,3.table.csv_"
    education_file = "data/raw/_ARDECO-RPDTN.versions_2024-unit_PC-isced11_ED0-2,ED3_4,ED5-8-age_Y25-64-sex_TOTAL-level_id_0,1,2.table.csv_"

    print("Cargando datos de ARDECO...")

    # Cargar y limpiar cada archivo
    df_unemployment = load_ardeco_file(unemployment_file, 'unemployment')
    df_gdp = load_ardeco_file(gdp_file, 'gdp')
    
    # Para educación solo cargamos nivel universitario ED5-8
    df_education = load_ardeco_file(education_file, 'education', education_level='ED5-8')

    print("Guardando en PostgreSQL...")

    # Guardar en PostgreSQL
    save_to_postgres(df_unemployment, 'ardeco_unemployment')
    save_to_postgres(df_gdp, 'ardeco_gdp')
    save_to_postgres(df_education, 'ardeco_education')

    print("✓ Proceso completado")sii