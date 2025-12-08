# config/uax.py (copied for Multitenant demo)
import os
from .base import PG_CONFIG_BASE, REGION

UAX_CONFIG = {
    "CODE": "uax",
    "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY_UAX"),
    "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY_UAX"),
    "AWS_ACCESS_KEY_SAND": os.getenv("AWS_ACCESS_KEY_SAND_UAX"),
    "AWS_SECRET_KEY_SAND": os.getenv("AWS_SECRET_KEY_SAND_UAX"),
    "REGION": REGION,
    "BUCKET_NAME": "foris-data-transfer-hub",
    "BUCKET_NAME_SAND": "foris-data-transfer-hub-sandbox",
    "TOKEN": os.getenv("UAX_TOKEN"),
    "PIPELINE_CODE": "darwin/publisher_pbi",
    "API_URL_BASE": "https://uax.piper.api.foris.ai",
    "TENANT_SUBDOMAIN": "uax",
    "CLIENT_ID": "uax",
    "EXTENSION_A_DESCARGAR": ".parquet",
    "CARPETA_METODO": r"C:\UAX",
    "ENTIDADES": [
        "pbi_d1_infraestructura_master",
        "pbi_d2_asignaturas_master",
        "pbi_d3_1_docentes_master",
        "pbi_d3_2_docentes_asignaturas_master",
        "pbi_d3_3_docentes_disponibilidad_master",
        "pbi_d4_festivos_master",
        "pbi_h1_grupos_master",
        "pbi_h2_horarios_master",
        "pbi_h3_reservas_master",
        "pbi_h4_inscripcion_master"
    ],
    "SCHEMA": "UAX",
    "TABLE_MASTER": '"UAX".table_master_uax',
    "DATALAKE_TABLE": '"UAX".datalake_parquet',
    "DWH_TARGET_SCHEMA": "UAX",
    "DWH_MAPEO_TABLAS": {
        "d1_infraestructura_master": "UAX_D1_INFRAESTRUCTURA",
        "d2_asignaturas_master": "UAX_D2_ASIGNATURAS",
        "d3_1_docentes_master": "UAX_D3_1_DOCENTES",
        "d3_2_docentes_asignaturas_master": "UAX_D3_2_DOCENTES_ASIGNATURAS",
        "d3_3_docentes_disponibilidad_master": "UAX_D3_3_DOCENTES_DISPONIBILIDAD",
        "d4_festivos_master": "UAX_D4_FESTIVOS",
        "h1_grupos_master": "UAX_H1_GRUPOS",
        "h2_horarios_master": "UAX_H2_HORARIOS",
        "h3_reservas_master": "UAX_H3_RESERVAS",
        "h4_inscripcion_master": "UAX_H4_INSCRIPCION",
    }
}
