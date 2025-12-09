
import os
import uuid
import traceback
import logging
from commons.data_transforms import convert_csv_to_parquet
# Importar configuración y servicios
from config.Bank_1 import BANK_1_CONFIG

logger = logging.getLogger(__name__)
from config.Bank_2 import BANK_2_CONFIG
from services.Database import db_queries
from services.Amazon import s3_storage
from services.Pipelines import pipeline_manager
from services.Database import db_connector 

# Diccionario de CONFIGURACIONES de disponibles
ENTIDAD_FINANCIERA = {
    BANK_1_CONFIG["CODE"]: BANK_1_CONFIG,
    BANK_2_CONFIG["CODE"]: BANK_2_CONFIG,
}
async def procesar_datalake_bancario(bank_code: str):
    """Ejecuta el datalake de cada banco"""
    config = ENTIDAD_FINANCIERA.get(bank_code.lower())
    if not config:
        logger.error("Configuracion no encontrada para banco: %s", bank_code)
        return
    logger.info("Iniciando datalake proceso por banco: %s", bank_code.upper())
    try:
        #Leer registros
        registros = db_queries.leer_table_master(config)
        extension_a_descargar = config["EXTENSION_A_DESCARGAR"]
        tenant = config["TENANT_SUBDOMAIN"]
        #aqui igual nomas es quitarle el _3
        if tenant.endswith("_2"):
            tenant= "Bank_2"
        for reg in registros:
            entorno = reg["entorno"].lower()
            
            #Ejecutar Pipeline
            integration_run_id = str(uuid.uuid4())
            resultadouuid = await pipeline_manager.ejecutar_pipeline(
                reg["escenario"], entorno, integration_run_id, reg["proceso"], config
            )
            if not resultadouuid: continue
            #Procesar entidades y descargar archivos.
            for entidad in config["ENTIDADES"]:
                # La construcción del prefix S3
                prefix_s3 = f"{tenant}/publisher/{'pbi/' if tenant == 'bank_1' else ''}{entidad}/integration_run_id={resultadouuid}"
                
                archivos_descargados = await s3_storage.descargar_archivos_de_s3(
                    prefix_s3, entorno, reg, entidad, extension_a_descargar, config
                )

                #Inserción en Datalake
                if archivos_descargados:
                    conn_ins = db_connector.get_db_connection()
                    try:
                        for ruta_archivo_descargado in archivos_descargados:
                            ruta_a_insertar = ruta_archivo_descargado
                            
                            # Conversión de CSV a Parquet si es necesario 
                            if extension_a_descargar == ".csv":
                                base, _ = os.path.splitext(ruta_archivo_descargado)
                                ruta_parquet = f"{base}.parquet"
                                
                                if convert_csv_to_parquet(ruta_archivo_descargado, ruta_parquet):
                                    ruta_a_insertar = ruta_parquet
                                    if os.path.exists(ruta_archivo_descargado):
                                        os.remove(ruta_archivo_descargado)
                                
                            # Insertamos la referencia a la ruta del archivo
                            db_queries.insert_datalake_reference(
                                reg, conn_ins, entidad, ruta_a_insertar, config
                            )
                            logger.debug("Datalake Referencia insertada: %s", os.path.basename(ruta_a_insertar))

                    except Exception as e:
                        logger.error("Falló el procesamiento o inserción: %s", e, exc_info=True)
                    finally:
                        conn_ins.close()
        logger.info("Datalake proceso completado para: %s", bank_code.upper())
        return True # Retorna True si el procesamiento del datalake fue exitoso
    except Exception as e:
        logger.error("Un error crítico ocurrió: %s", e, exc_info=True)
        