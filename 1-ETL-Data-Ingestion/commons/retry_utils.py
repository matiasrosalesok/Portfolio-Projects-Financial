"""
Utilidades de reintentos con backoff exponencial.
Proporciona decoradores para reintentos robustos en operaciones de red.
"""

import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result,
)

logger = logging.getLogger(__name__)

# Configuración de reintentos para operaciones de S3
S3_RETRY_CONFIG = {
    "stop": stop_after_attempt(5),  # Máximo 5 intentos
    "wait": wait_exponential(multiplier=1, min=2, max=30),  # 2s, 4s, 8s, 16s, 30s
    "retry": retry_if_exception_type((
        ConnectionError,
        TimeoutError,
        IOError,
        OSError,
    )),
}

# Configuración de reintentos para Pipeline API
PIPELINE_RETRY_CONFIG = {
    "stop": stop_after_attempt(4),  # Máximo 4 intentos
    "wait": wait_exponential(multiplier=1, min=3, max=30),  # 3s, 6s, 12s, 30s
    "retry": retry_if_exception_type((
        ConnectionError,
        TimeoutError,
        IOError,
    )),
}


def retry_s3_operation(func):
    """
    Decorador para reintentos en operaciones S3.
    Reintenta hasta 5 veces con backoff exponencial (2-30s).
    """
    @retry(**S3_RETRY_CONFIG)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Operation {func.__name__} succeeded")
            return result
        except Exception as e:
            logger.warning(f"Operation {func.__name__} failed: {e}. Retrying...")
            raise
    
    return wrapper


def retry_pipeline_operation(func):
    """
    Decorador para reintentos en llamadas a Pipeline API.
    Reintenta hasta 4 veces con backoff exponencial (3-30s).
            ...
    """
    @retry(**PIPELINE_RETRY_CONFIG)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Operation {func.__name__} succeeded")
            return result
        except Exception as e:
            logger.warning(f"Operation {func.__name__} failed: {e}. Retrying...")
            raise
    
    return wrapper
