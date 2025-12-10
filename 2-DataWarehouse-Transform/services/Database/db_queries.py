# services/db_queries.py (for DataWarehouse demo)
import logging
from services.Database.db_connector import get_db_connection

logger = logging.getLogger(__name__)

def leer_table_master(config: dict) -> list:
    table_name = config["TABLE_MASTER"]
    query = f"""
        SELECT coordenada_key, ambiente, periodo, escenario, proceso, demanda, entorno
        FROM {table_name};
    """
    conn = get_db_connection()
    try:
        logger.debug("Leyendo table_master from %s", table_name)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        logger.debug("Leído table_master: %d records", len(rows))

        return [
            {
                "coordenada_key": row[0],
                "ambiente":       row[1],
                "periodo":        row[2],
                "escenario":      row[3],
                "proceso":        row[4],
                "demanda":        row[5],
                "entorno":        row[6],
            } for row in rows
        ]
    finally:
        conn.close()


def insert_datalake_reference(reg: dict, conn, entidad: str, file_path: str, config: dict):
    table_name = config["DATALAKE_TABLE"]
    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO {table_name}
                (ambiente, periodo, scenario, proceso, demanda, entidad, entorno, "timestamp", data)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, now(), %s);
        """, (
            reg["ambiente"], reg["periodo"], reg["escenario"], reg["proceso"], 
            reg["demanda"], entidad, reg["entorno"], file_path
        ))
    conn.commit()
# services/db_queries.py
import logging
from services.Database.db_connector import get_db_connection

logger = logging.getLogger(__name__)

def leer_table_master(config: dict) -> list:
    """Lee registros de la tabla master de la entidad financiera actual."""
    table_name = config["TABLE_MASTER"]
    query = f"""
        SELECT coordenada_key, ambiente, periodo, escenario, proceso, demanda, entorno
        FROM {table_name};
    """
    conn = get_db_connection()
    try:
        logger.debug("Leyendo table_master from %s", table_name)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        logger.debug("Leído table_master: %d records", len(rows))

        return [
            {
                "coordenada_key": row[0],
                "ambiente":       row[1],
                "periodo":        row[2],
                "escenario":      row[3],
                "proceso":        row[4],
                "demanda":        row[5],
                "entorno":        row[6],
            } for row in rows
        ]
    finally:
        conn.close()


def insert_datalake_reference(reg: dict, conn, entidad: str, file_path: str, config: dict):
    """Inserta la referencia al archivo en la tabla de metadatos (datalake_parquet)."""
    table_name = config["DATALAKE_TABLE"]
    
    # ... (Tu lógica de limpieza/conversión a string de las variables) ...
    
    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO {table_name}
                (ambiente, periodo, scenario, proceso, demanda, entidad, entorno, "timestamp", data)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, now(), %s);
        """, (
            reg["ambiente"], reg["periodo"], reg["escenario"], reg["proceso"], 
            reg["demanda"], entidad, reg["entorno"], file_path
        ))
    conn.commit()
