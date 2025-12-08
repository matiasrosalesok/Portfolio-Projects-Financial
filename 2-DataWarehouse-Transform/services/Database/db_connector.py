# services/db_connector.py
import psycopg2
from config.base import PG_CONFIG_BASE

def get_db_connection():
    """Retorna una nueva conexión de PostgreSQL usando la configuración base."""
    return psycopg2.connect(**PG_CONFIG_BASE)
