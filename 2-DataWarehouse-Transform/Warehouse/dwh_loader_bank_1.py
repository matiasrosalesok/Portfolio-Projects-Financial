# dwh_loader_bank_1.py
from config.bank_1 import INSTITUTION_A_CONFIG
from Warehouse.dwh_core import run_dwh_loader

def run_bank_1_dwh_loader():
    """Ejecuta la carga DWH usando la configuración."""
    run_dwh_loader(INSTITUTION_A_CONFIG)

if __name__ == "__main__":
    run_bank_1_dwh_loader()

