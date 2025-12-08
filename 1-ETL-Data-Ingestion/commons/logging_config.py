"""
Configuración centralizada de logging para el proyecto.
Define formato y niveles de log para desarrollo y producción.
"""
import logging
import logging.handlers
import os
from pathlib import Path

# Crear directorio de logs si no existe
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Nombre de archivo de log
LOG_FILE = LOG_DIR / "app.log"

# Formato de log
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging(level=logging.INFO, log_to_file=True):
    """
    Configura el logging para el proyecto.
    
    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Si True, también escribe a archivo
    """
    # Obtener el root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Limpiar handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # Handler console (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Handler archivo (con rotación)
    if log_to_file:
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10_000_000,  # 10 MB
            backupCount=5  # Mantener 5 archivos
        )
        file_handler.setLevel(logging.DEBUG)  # Archivo siempre en DEBUG
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger

# Detectar nivel desde variable de entorno
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
NUMERIC_LOG_LEVEL = getattr(logging, LOG_LEVEL, logging.INFO)

# Configurar al importar
setup_logging(level=NUMERIC_LOG_LEVEL, log_to_file=True)
