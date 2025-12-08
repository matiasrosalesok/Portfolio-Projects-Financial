"""Run a tiny import sanity check for Analytics subproject."""
import sys
print('Analytics demo starting')
try:
    import evolutivos.evolutivos_ue as ev
    print('Imports OK: evolutivos_ue')
    print('Python:', sys.version.splitlines()[0])
except Exception as e:
    print('Import failed:', e)
    raise
