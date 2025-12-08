"""Run a tiny import sanity check for the DataWarehouse subproject."""
import sys
print('DataWarehouse demo starting')
try:
    import services.Database.db_connector as dbc
    import Warehouse.dwh_core as core
    print('Imports OK: db_connector, dwh_core')
    print('Python:', sys.version.splitlines()[0])
except Exception as e:
    print('Import failed:', e)
    raise
