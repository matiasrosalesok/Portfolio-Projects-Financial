import pandas as pd
from sqlalchemy import create_engine
from config.base import PG_CONFIG_BASE
from config.uag import UAG_CONFIG

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{PG_CONFIG_BASE['user']}:{PG_CONFIG_BASE['password']}@"
        f"{PG_CONFIG_BASE['host']}:{PG_CONFIG_BASE['port']}/{PG_CONFIG_BASE['dbname']}"
    )

def sample_metric(engine, schema):
    SQL = f"SELECT * FROM \"{schema}\".UE_INT_DOCENTES LIMIT 10"
    df = pd.read_sql(SQL, engine)
    return df.head()
