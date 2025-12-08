"""Run a tiny import sanity check for PowerBI subproject."""
import sys
print('PowerBI demo starting')
try:
    import scripts.export_powerbi_dataset as ex
    print('Imports OK: export_powerbi_dataset')
    print('Python:', sys.version.splitlines()[0])
except Exception as e:
    print('Import failed:', e)
    raise
