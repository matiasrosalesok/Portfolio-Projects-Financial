"""Run a tiny import sanity check for the ETL subproject."""
import sys
print('ETL demo starting')
try:
    import commons.logging_config as lc
    import commons.data_transforms as dt
    import services.Pipelines.pipeline_manager as pm
    print('Imports OK: logging_config, data_transforms, pipeline_manager')
    print('Python:', sys.version.splitlines()[0])
except Exception as e:
    print('Import failed:', e)
    raise
