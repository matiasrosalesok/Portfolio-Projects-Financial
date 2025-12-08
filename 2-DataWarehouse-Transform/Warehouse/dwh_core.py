# dwh_core.py (copied for DataWarehouse demo)
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from config.base import PG_CONFIG_BASE
from commons.data_transforms import safe_read_parquet, normalize_dtypes_for_postgres, copy_to_postgres, cargar_mapa_coordenadas
from commons.transformaciones_por_universidad import transformar_por_universidad

logger = logging.getLogger(__name__)

def run_dwh_loader(config: dict):
    """
    Ejecuta la carga de datos del Datalake al DWH para una universidad específica,
    basándose en su diccionario de configuración.
    """
    
    ENTIDADES = config["ENTIDADES"]
    MAPEO_TABLAS = config["DWH_MAPEO_TABLAS"]
    TARGET_SCHEMA = config["DWH_TARGET_SCHEMA"]
    DATALAKE_TABLE = config["DATALAKE_TABLE"]
    TABLE_MASTER = config["TABLE_MASTER"]
    REEMPLAZAR_TABLAS = True

    # 1. Conexión a la Base de Datos
    engine = create_engine(
        f"postgresql+psycopg2://{PG_CONFIG_BASE['user']}:{PG_CONFIG_BASE['password']}@"
        f"{PG_CONFIG_BASE['host']}:{PG_CONFIG_BASE['port']}/{PG_CONFIG_BASE['dbname']}"
    )
    conn_pg = engine.raw_connection()
    cursor = conn_pg.cursor()

    # Asegura que el esquema exista
    with engine.connect() as eg:
        eg.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{TARGET_SCHEMA}";'))

    # 2. Query para obtener la última versión del día (usando la tabla DATALAKE_TABLE específica)
    SQL_LATEST = f'''
        WITH ranked AS (
            SELECT
                scenario, entidad, entorno, ambiente, proceso, periodo, demanda,
                data AS file_path, "timestamp",
                ROW_NUMBER() OVER (
                    PARTITION BY scenario, entidad, entorno, ambiente, proceso, periodo ,demanda
                    ORDER BY "timestamp" DESC
                ) AS rn
            FROM {DATALAKE_TABLE}
            WHERE entidad = %s
              AND "timestamp" >= CURRENT_DATE -- Filtrar por hoy
              AND "timestamp" < CURRENT_DATE + INTERVAL '1 day'
        )
        SELECT scenario, entidad, entorno, ambiente, proceso, periodo,demanda, file_path, "timestamp"
        FROM ranked
        WHERE rn = 1
        ORDER BY scenario, entorno, ambiente, proceso, periodo,demanda;
    '''
    mapa = cargar_mapa_coordenadas(engine, TABLE_MASTER)
    
    # 3. Proceso de Carga
    total_entidades = 0
    total_archivos = 0

    try:
        for entidad in ENTIDADES:
            logger.info("Procesando Entidad: %s", entidad)
            cursor.execute(SQL_LATEST, (entidad,))
            rows = cursor.fetchall()

            if not rows:
                logger.warning("sin rutas parquet recientes en el datalake para esta entidad: %s", entidad)
                continue

            primero = True
            archivos_leidos = 0
            
            for scenario, entidad_, entorno, ambiente, proceso, periodo, demanda, file_path, fecha_creacion in rows:
                df = safe_read_parquet(file_path)
                logger.debug("Archivo Parquet leído: %s shape=%s", file_path, df.shape)
                if df.empty:
                    logger.warning("Empty dataframe for file: %s", file_path)
                    continue
                df["fecha_creacion"] = fecha_creacion 
                df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"], errors="coerce").dt.strftime("%d/%m/%Y")
                df = transformar_por_universidad(df, config["CODE"])
                scenario_s = str(scenario).strip()
                proceso_s  = str(proceso).strip()
                demanda_s  = str(demanda).strip()
                entorno_s  = (entorno or "").strip().lower()
                ambiente_s = (ambiente or "").strip().lower()
                periodo_s  = (periodo or "").strip().lower()

                key_tuple = (scenario_s, entorno_s, ambiente_s, proceso_s, demanda_s, periodo_s)
                
                try:
                    coord_key = int(mapa.loc[key_tuple])
                except KeyError:
                    logger.error("No hay coordenada_key para scenario=%s entorno=%s ambiente=%s proceso=%s demanda=%s periodo=%s", 
                                 scenario_s, entorno_s, ambiente_s, proceso_s, demanda_s, periodo_s)
                    continue                

                df["COORDENADA_KEY"] = coord_key
                cols_rest = [c for c in df.columns if c != "COORDENADA_KEY"]
                df = df[["COORDENADA_KEY"] + cols_rest]
                df = normalize_dtypes_for_postgres(df)

                nombre_tabla = MAPEO_TABLAS.get(entidad, entidad)
                copy_to_postgres(df, engine, TARGET_SCHEMA, nombre_tabla, replace=primero and REEMPLAZAR_TABLAS)
                
                archivos_leidos += 1
                total_archivos += 1
                primero = False

                logger.info("COPY completed: table=%s.%s rows=%d", TARGET_SCHEMA, nombre_tabla, len(df))

            if archivos_leidos > 0:
                total_entidades += 1
                logger.info("Finalizaada entidad completed: %s files_processed=%d", nombre_tabla, archivos_leidos)

    finally:
        cursor.close()
        conn_pg.close()
        logger.info("DWH: Entidades_procesadas=%d files_read=%d", total_entidades, total_archivos)