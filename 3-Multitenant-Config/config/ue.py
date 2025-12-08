# config/ue.py (copied for Multitenant demo)
import os
from .base import PG_CONFIG_BASE, REGION

UE_CONFIG = {
    "CODE": "ue",
    "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY_UE"),
    "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY_UE"),
    "AWS_ACCESS_KEY_SAND": os.getenv("AWS_ACCESS_KEY_SAND_UE"),
    "AWS_SECRET_KEY_SAND": os.getenv("AWS_SECRET_KEY_SAND_UE"),
    "REGION": REGION,
    "TOKEN": os.getenv("UE_TOKEN"),
    "PIPELINE_CODE": "darwin/pbi/all/by_origin_ids",
    "API_URL_BASE": "https://ueuropea.piper.api.foris.ai",
    "TENANT_SUBDOMAIN": "ueuropea",
    "CLIENT_ID": "ueuropea",
    "EXTENSION_A_DESCARGAR": ".parquet",
    "CARPETA_METODO": r"C:\UE",
    "ENTIDADES": [
        "courses_pbi",
        "instructors_pbi",
        "infrastructure_pbi",
        "instructors_courses_pbi",
        "instructors_availability_pbi",
        "schedules_pbi",
        "groups_pbi"
    ],
    "SCHEMA": "UE",
    "TABLE_MASTER": '"UE"."UE_ACT_CONTEXTO"',
    "DATALAKE_TABLE": '"UE".datalake_parquet',
    "DWH_TARGET_SCHEMA": "UE",
    "DWH_MAPEO_TABLAS": {
        "infrastructure_pbi": "UE_INT_INFRAESTRUCTURA",
        "instructors_pbi": "UE_INT_DOCENTES",
        "courses_pbi": "UE_INT_ASIGNATURAS",
        "schedules_pbi": "UE_INT_HORARIOS",
        "groups_pbi": "UE_INT_GRUPOS",
        "instructors_courses_pbi": "UE_INT_DOCENTES_ASIGNATURAS",
        "instructors_availability_pbi": "UE_INT_DOCENTES_DISPONIBILIDAD"
    }
}
