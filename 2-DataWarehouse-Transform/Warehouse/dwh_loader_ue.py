# dwh_loader_ue.py
from config.ue import UE_CONFIG
from Warehouse.dwh_core import run_dwh_loader

def run_ue_dwh_loader():
    """Ejecuta la carga DWH usando la configuración de la UE."""
    run_dwh_loader(UE_CONFIG)

if __name__ == "__main__":
    run_ue_dwh_loader()
# dwh_loader_ue.py
from config.ue import UE_CONFIG
from Warehouse.dwh_core import run_dwh_loader

# Para que el main.py pueda importarlo fácilmente y llamarlo con el config
def run_ue_dwh_loader():
    """Ejecuta la carga DWH usando la configuración de la UE."""
    run_dwh_loader(UE_CONFIG)

if __name__ == "__main__":
    run_ue_dwh_loader()
