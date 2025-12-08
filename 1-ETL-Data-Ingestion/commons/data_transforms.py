# commons/data_transforms.py
import pandas as pd
import io
from sqlalchemy.engine import Engine
from sqlalchemy import text

# =========================
# Helpers
# =========================

def safe_read_parquet(path: str) -> pd.DataFrame:
    """Lee un archivo Parquet de forma segura, retornando un DataFrame vacío si falla."""
    try:
        df = pd.read_parquet(path, engine='pyarrow')
        return df
    except Exception as e:
        print(f"Error leyendo parquet {path}: {e}")
        return pd.DataFrame()

def normalize_dtypes_for_postgres(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in df.columns:
        # Convertir floats a enteros
        if pd.api.types.is_float_dtype(df[c]):
            s = df[c].dropna()
            if len(s) == 0 or ((s % 1).abs() < 1e-9).all():
                df[c] = pd.to_numeric(df[c], errors='coerce').round().astype('Int64')
        if pd.api.types.is_object_dtype(df[c]):
            df[c] = df[c].astype("string")
    return df

def copy_to_postgres(df: pd.DataFrame, engine: Engine, schema: str, table: str, replace: bool = True):
    """
    Carga un DataFrame a PostgreSQL usando la sentencia COPY para optimizar la velocidad.
    """
    if df.empty:
        print(f"DataFrame vacío para {schema}.{table}. Saltando COPY.")
        return

    #Crear/Reemplazar la estructura de la tabla
    if replace:
        # Usamos to_sql con if_exists='replace' para manejar la creación de la tabla
        df.head(0).to_sql(table, engine, schema=schema, if_exists="replace", index=False)
        
    #Uso de COPY para inserción masiva
    buffer = io.StringIO()
    df.to_csv(buffer, sep='\t', index=False, header=False, na_rep='NULL_VAL') 
    buffer.seek(0)

    # Obtenemos la conexión raw
    raw = engine.raw_connection()
    try:
        with raw.cursor() as cur:
            cur.copy_expert(
                f"""
                COPY "{schema}"."{table}" FROM STDIN WITH (
                    FORMAT CSV, DELIMITER E'\\t', NULL 'NULL_VAL'
                )
                """,
                buffer
            )
        raw.commit()
    except Exception as e:
        raw.rollback()
        raise e
    finally:
        raw.close()
        
def convert_csv_to_parquet(csv_path: str, parquet_path: str) -> bool:
    """
    Lee un archivo CSV y lo guarda como un archivo Parquet.
    Utiliza el delimitador '|' (pipe) para la lectura.
    Retorna True si la conversión fue exitosa, False en caso contrario.
    """
    try:
        # La lectura usa sep='|' como se definió en el código anterior
        df = pd.read_csv(csv_path, sep='|', header=0)
        df.to_parquet(parquet_path, engine='pyarrow', index=False)
        return True
    except Exception as e:
        print(f"Falló la conversión de CSV a Parquet para {csv_path}: {e}")
        return False
    

def cargar_mapa_coordenadas(engine, table_master):
    SQL_MASTER = f'''
        SELECT
          coordenada_key,
          escenario AS scenario,
          entorno,
          ambiente,
          proceso,
          demanda,
          periodo
        FROM {table_master};
    '''

    mapa_df = pd.read_sql(SQL_MASTER, engine)

    # normalizar
    mapa_df["scenario"] = mapa_df["scenario"].astype(str).str.strip()
    mapa_df["proceso"]  = mapa_df["proceso"].astype(str).str.strip()
    mapa_df["demanda"]  = mapa_df["demanda"].astype(str).str.strip()
    mapa_df["entorno"]  = mapa_df["entorno"].astype(str).str.strip().str.lower()
    mapa_df["ambiente"] = mapa_df["ambiente"].astype(str).str.strip().str.lower()
    mapa_df["periodo"]  = mapa_df["periodo"].astype(str).str.strip().str.lower()

    idx_cols = ["scenario", "entorno", "ambiente", "proceso", "demanda", "periodo"]

    mapa = (
        mapa_df
        .drop_duplicates(subset=idx_cols)
        .set_index(idx_cols)["coordenada_key"]
    )

    return mapa
