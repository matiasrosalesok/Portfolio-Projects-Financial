# dwh_loader_bank_2.py
from config.bank_2 import INSTITUTION_B_CONFIG
from Warehouse.dwh_core import run_dwh_loader

def run_bank_2_dwh_loader():
    """Ejecuta la carga DWH usando la configuración de la uag."""
    run_dwh_loader(INSTITUTION_B_CONFIG)

if __name__ == "__main__":
    run_bank_2_dwh_loader()
