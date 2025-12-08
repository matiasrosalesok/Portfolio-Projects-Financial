import os
from .base import PG_CONFIG_BASE, REGION

UAG_CONFIG = {
    "CODE": "uag",
    "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY_UAG"),
    "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY_UAG"),
    "AWS_ACCESS_KEY_SAND": os.getenv("AWS_ACCESS_KEY_SAND_UAG"),
    "AWS_SECRET_KEY_SAND": os.getenv("AWS_SECRET_KEY_SAND_UAG"),
    "REGION": REGION,
    "BUCKET_NAME": "foris-data-transfer-hub",
    "BUCKET_NAME_SAND": "foris-data-transfer-hub-sandbox",
    "TOKEN": os.getenv("UAG_TOKEN"),
    "PIPELINE_CODE": "darwin/publisher_pbi/generic",
    "API_URL_BASE": "https://uag-mx.piper.api.foris.ai",
    "TENANT_SUBDOMAIN": "uag-mx",
    "CLIENT_ID": "uag",
    "EXTENSION_A_DESCARGAR": ".parquet",
    "CARPETA_METODO": r"C:\UAG",
    "ENTIDADES": [
        "d1_infraestructura_master",
        "d2_asignaturas_master",
        "d3_1_docentes_master",
        "d3_2_docentes_asignaturas_master",
        "d3_3_docentes_disponibilidad_master",
        "d4_festivos_master",
        "h1_grupos_master",
        "h2_horarios_master",
        "h3_reservas_master",
        "h4_inscripcion_master"
    ],
    "SCHEMA": "UAG",
    "TABLE_MASTER": '"UAG".UAG_ACT_CONTEXTO',
    "DATALAKE_TABLE": '"UAG".datalake_parquet',
    "DWH_TARGET_SCHEMA": "UAG",
    "DWH_MAPEO_TABLAS": {
        "d1_infraestructura_master": "UAG_INT_INFRAESTRUCTURA",
        "d3_1_docentes_master": "UAG_INT_DOCENTES",
        "d2_asignaturas_master": "UAG_INT_ASIGNATURAS",
        "h2_horarios_master": "UAG_INT_HORARIOS",
        "h1_grupos_master": "UAG_INT_GRUPOS",
        "d3_2_docentes_asignaturas_master": "UAG_INT_DOCENTES_ASIGNATURAS",
        "d3_3_docentes_disponibilidad_master": "UAG_INT_DOCENTES_DISPONIBILIDAD"
    }
}
