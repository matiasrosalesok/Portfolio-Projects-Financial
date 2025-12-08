"""Run a tiny import sanity check for Multitenant config subproject."""
import sys
print('Multitenant demo starting')
try:
    import config.base as base
    import config.ue as ue
    print('Imports OK: config.base, config.ue')
    print('Python:', sys.version.splitlines()[0])
except Exception as e:
    print('Import failed:', e)
    raise
