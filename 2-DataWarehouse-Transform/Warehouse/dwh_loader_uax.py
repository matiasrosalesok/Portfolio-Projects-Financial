# dwh_loader_uax.py
from config.uax import UAX_CONFIG
from Warehouse.dwh_core import run_dwh_loader

def run_uax_dwh_loader():
    """Ejecuta la carga DWH usando la configuración de la UAX."""
    run_dwh_loader(UAX_CONFIG)

if __name__ == "__main__":
    run_uax_dwh_loader()
