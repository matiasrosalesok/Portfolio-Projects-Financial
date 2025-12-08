# services/s3_storage.py (copied for portfolio ETL demo)
import os
import boto3
import botocore.exceptions
import logging
from datetime import datetime
from config.base import AWS_BUCKETS, REGION
from commons.retry_utils import retry_s3_operation

logger = logging.getLogger(__name__)


@retry_s3_operation
def _download_file_with_retry(s3_client, bucket, key, local_path):
    """Descarga un archivo de S3 con reintentos automáticos."""
    s3_client.download_file(bucket, key, local_path)


async def descargar_archivos_de_s3(
    prefix: str, entorno: str, reg: dict, entidad: str, extension: str, config: dict
):
    """
    Busca y descarga archivos de S3, usando las credenciales y rutas bancarias.
    Usa paginación, retry logic, y no imprime credenciales en stdout.
    """

    # Determinar credenciales y bucket
    is_sandbox = entorno.lower() == "sandbox"
    aws_access_key = config.get("AWS_ACCESS_KEY_SAND") if is_sandbox else config.get("AWS_ACCESS_KEY")
    aws_secret_key = config.get("AWS_SECRET_KEY_SAND") if is_sandbox else config.get("AWS_SECRET_KEY")
    bucket = AWS_BUCKETS["sandbox"] if is_sandbox else AWS_BUCKETS["prod"]
    carpeta_metodo = config.get("CARPETA_METODO", ".")

    # Registrar información no sensible
    logger.debug("S3 download: bucket=%s prefix=%s entidad=%s entorno=%s", bucket, prefix, entidad, entorno)

    s3 = boto3.client(
        "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=REGION
    )

    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    archivos_descargados = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    os.makedirs(carpeta_metodo, exist_ok=True)

    try:
        found_any = False
        for page in page_iterator:
            contents = page.get("Contents", [])
            if not contents:
                continue
            for obj in contents:
                key = obj.get("Key")
                if not key:
                    continue
                if not key.endswith(extension):
                    continue

                found_any = True
                nombre_local = (
                    f"raw_{entidad}_{entorno}_{reg.get('ambiente')}_{reg.get('escenario')}_"
                    f"{reg.get('proceso')}_{reg.get('demanda')}_{timestamp}{extension}"
                )
                ruta_local = os.path.join(carpeta_metodo, nombre_local)

                try:
                    # Usar función con retry automático
                    _download_file_with_retry(s3, bucket, key, ruta_local)
                    archivos_descargados.append(ruta_local)
                    logger.info("Descargado: %s", os.path.basename(ruta_local))
                except Exception as e:
                    logger.error("ERROR al descargar %s después de reintentos: %s", key, e)

        if not found_any:
            logger.warning("No se encontraron archivos para %s con prefijo %s", entidad, prefix)
    except botocore.exceptions.BotoCoreError as e:
        logger.error("Error listando objetos en S3: %s", e)

    return archivos_descargados
