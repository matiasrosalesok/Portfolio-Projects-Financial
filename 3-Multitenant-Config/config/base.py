import os
from pathlib import Path
from dotenv import load_dotenv

# ==============================================================
# Carga variables de entorno desde .env (raíz del proyecto)
# ==============================================================
ENV_FILE = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=str(ENV_FILE))

# ==============================================================
# CONFIGURACIÓN BASE DE POSTGRESQL (DWH/DATALAKE)
# Las variables se cargan desde el archivo .env (obligatorio)
# ==============================================================
PG_CONFIG_BASE = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": int(os.getenv("PG_PORT", "5433")),
    "dbname": os.getenv("PG_DBNAME"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD")
}

AWS_BUCKETS = {
    "prod": "banking-data-transfer-hub",
    "sandbox": "banking-data-transfer-hub-sandbox"
}
REGION = os.getenv("AWS_REGION", "us-east-1")
