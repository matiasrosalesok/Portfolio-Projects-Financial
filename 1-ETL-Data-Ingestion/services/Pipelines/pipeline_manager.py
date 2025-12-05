# services/pipeline_manager.py
import requests
import asyncio
import logging
from datetime import datetime, timedelta
from commons.retry_utils import retry_pipeline_operation

logger = logging.getLogger(__name__)

def construir_args(escenario, entorno, proceso, config: dict):
    """Construye los argumentos del pipeline."""
    tenant = config["TENANT_SUBDOMAIN"]
    client = config["CLIENT_ID"]
    
    base = {
        "client": client,
        #aqui para el pipe general nomas es quitarle el -mx
        "organization": f"{client}-es" if client == "uax" else f"{client}" if client == "uag" else client,
        "tenant": tenant,
        "env": f"{entorno}",
        "origin_ids": f"{proceso}",
        "scenario_id": f"{escenario}",
    }
    return str(base)


@retry_pipeline_operation
def _ejecutar_pipeline_request(token, api_base, pipeline_code, tenant_subdomain, integration_run_id, args_str):
    """Realiza la petición HTTP de ejecución con reintentos."""
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(
        f"{api_base}/api/v1/pipelines/run/", headers=headers, timeout=15,
        json={
            "ARGS": args_str, 
            "PIPELINE_CODE": pipeline_code, 
            "INTEGRATION_RUN_ID": integration_run_id,
            "PIPER_BACKEND_TENANT_SUBDOMAIN": tenant_subdomain,
            "timeout": 80000
        }
    )
    response.raise_for_status()
    return response


@retry_pipeline_operation
def _consultar_pipeline_status(token, api_base, pipeline_code, fechaAfter, fechaBefore):
    """Consulta el estado del pipeline con reintentos."""
    headers = {"Authorization": f"Token {token}"}
    endpointConsultar = (
        f"{api_base}/api/v1/pipeline-run/"
        f"?pipeline_code={pipeline_code}&inserted_at_after={fechaAfter}"
        f"&inserted_at_before={fechaBefore}&size=1000"
    )
    resp = requests.get(endpointConsultar, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


async def ejecutar_pipeline(escenario, entorno, integration_run_id, proceso, config: dict, poll_seconds=30):
    """Ejecuta el pipeline de Foris y espera a que termine (polling con reintentos)."""
    
    # Cargar variables de la configuración
    token = config["TOKEN"]
    pipeline_code = config["PIPELINE_CODE"]
    api_base = config["API_URL_BASE"]
    tenant_subdomain = config["TENANT_SUBDOMAIN"]

    args_str = construir_args(escenario, entorno, proceso, config)
    
    try:
        # Petición de Ejecución (con reintentos)
        logger.debug("Ejecución pipeline: pipeline_code=%s tenant=%s", pipeline_code, tenant_subdomain)
        _ejecutar_pipeline_request(token, api_base, pipeline_code, tenant_subdomain, integration_run_id, args_str)

        # Bucle de Monitoreo (Polling)
        fechaAfter = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
        fechaBefore = (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")
        
        while True:
            # Consulta con reintentos
            data = _consultar_pipeline_status(token, api_base, pipeline_code, fechaAfter, fechaBefore)
            items = data.get("items", [])
            
            target = next((it for it in items if it.get("integration_run_id") == integration_run_id), None)
            
            if target:
                status = target.get("status")
                if status == "DONE":
                    logger.info("Estado ejecución completo: integration_run_id=%s", integration_run_id)
                    return target["integration_run_id"]
                
                if status != "RUN":
                    logger.error("Estado ejecución fallo con status: %s", status)
                    return None
            
            state_msg = "RUN" if target else "No encontrado, reintentando"
            logger.debug("Pipeline status polling: state=%s waiting_seconds=%d", state_msg, poll_seconds)
            await asyncio.sleep(poll_seconds)

    except requests.exceptions.RequestException as e:
        logger.error("Error en la comunicación con el pipeline después de reintentos: %s", e, exc_info=True)
        return None
