import pandas as pd
import numpy as np
from datetime import datetime  
from sqlalchemy import create_engine
from config.base import PG_CONFIG_BASE
from config.ue import UE_CONFIG

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{PG_CONFIG_BASE['user']}:{PG_CONFIG_BASE['password']}@"
        f"{PG_CONFIG_BASE['host']}:{PG_CONFIG_BASE['port']}/{PG_CONFIG_BASE['dbname']}"
    )
    
def parse_tags_column(df, col_name="TAGS_DOCENTE", strip_prefix="ue.es/"):
    """
    Parsea una columna de texto con JSON y la expande a columnas normales.

    - df: DataFrame original
    - col_name: nombre de la columna con el JSON
    - strip_prefix: prefijo a eliminar de las claves del JSON
    """
    import json
    import pandas as pd

    def _parse_cell(value):
        if pd.isna(value):
            return {}
        text = str(value).replace('""', '"')
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {}

    tags_dict_series = df[col_name].apply(_parse_cell)
    tags_cols = pd.json_normalize(tags_dict_series)

    if strip_prefix:
        tags_cols.columns = [c.split('/', 1)[-1] for c in tags_cols.columns]

    df_out = pd.concat(
        [df.drop(columns=[col_name]), tags_cols],
        axis=1
    )

    return df_out

# (file continues with domain-specific functions — truncated in this demo copy)
