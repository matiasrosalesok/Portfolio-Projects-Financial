# dwh_loader_uag.py
from config.uag import UAG_CONFIG
from Warehouse.dwh_core import run_dwh_loader

def run_uag_dwh_loader():
    """Ejecuta la carga DWH usando la configuración de la uag."""
    run_dwh_loader(UAG_CONFIG)

if __name__ == "__main__":
    run_uag_dwh_loader()
