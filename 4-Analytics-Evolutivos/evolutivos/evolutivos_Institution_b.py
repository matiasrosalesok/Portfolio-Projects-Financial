"""
Analytics · Evolutivos for Institution_b (Bank Beta)

"""

from datetime import date
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from config.base import PG_CONFIG_BASE
from config.bank_2 import INSTITUTION_A_CONFIG


# ======================================================
# ENGINE & SCHEMA
# ======================================================

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{PG_CONFIG_BASE['user']}:{PG_CONFIG_BASE['password']}@"
        f"{PG_CONFIG_BASE['host']}:{PG_CONFIG_BASE['port']}/{PG_CONFIG_BASE['dbname']}"
    )


def _get_schema(config: dict, default_schema: str) -> str:
    return config.get("schema_analytics", default_schema) if isinstance(config, dict) else default_schema


# ======================================================
# LOAD BASE DATA
# ======================================================

def load_transactions(
    engine,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> pd.DataFrame:

    schema = _get_schema(INSTITUTION_A_CONFIG, "bank_beta_analytics")
    where_clauses = []
    params: Dict[str, object] = {}

    if start_date:
        where_clauses.append("transaction_date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where_clauses.append("transaction_date <= :end_date")
        params["end_date"] = end_date

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    sql = text(f"""
        SELECT transaction_date, product_category, transaction_channel,
               amount, account_id
        FROM "{schema}".int_transactions
        {where_sql}
    """)

    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params=params)

    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df


# ======================================================
# ANALYTICS
# ======================================================

def calculate_daily_aggregations(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    return (
        df.groupby(["transaction_date", "product_category", "transaction_channel"], dropna=False)
        .agg(
            daily_volume=("amount", "sum"),
            transaction_count=("amount", "count"),
            avg_transaction=("amount", "mean"),
            min_transaction=("amount", "min"),
            max_transaction=("amount", "max"),
            unique_accounts=("account_id", "nunique"),
            std_amount=("amount", "std"),
        )
        .reset_index()
    )


def calculate_monthly_evolution(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    df["year"] = df["transaction_date"].dt.year
    df["month"] = df["transaction_date"].dt.month

    monthly = (
        df.groupby(["year", "month", "product_category"], dropna=False)
        .agg(
            monthly_volume=("amount", "sum"),
            transaction_count=("amount", "count"),
        )
        .reset_index()
        .sort_values(["product_category", "year", "month"])
    )

    monthly["growth_rate"] = (
        monthly.groupby("product_category")["monthly_volume"].pct_change()
    )

    return monthly


def calculate_yoy_comparison(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    df["year"] = df["transaction_date"].dt.year

    yearly = (
        df.groupby(["year", "product_category"], dropna=False)
        .agg(yearly_volume=("amount", "sum"))
        .reset_index()
    )

    yearly = yearly.sort_values(["product_category", "year"])
    yearly["yoy_growth_percent"] = (
        yearly.groupby("product_category")["yearly_volume"].pct_change() * 100
    )

    return yearly


def calculate_global_kpis(df: pd.DataFrame) -> Dict[str, float]:
    if df.empty:
        return {
            "total_volume": 0.0,
            "transaction_count": 0,
            "avg_transaction": 0.0,
            "unique_accounts": 0,
        }

    return {
        "total_volume": float(df["amount"].sum()),
        "transaction_count": int(df["amount"].count()),
        "avg_transaction": float(df["amount"].mean()),
        "unique_accounts": int(df["account_id"].nunique()),
    }


# ======================================================
# APPEND EVOLUTIVO
# ======================================================

def _delete_rows(engine, schema: str, table: str, column: str, values):
    sql = text(f"""DELETE FROM "{schema}".{table} WHERE {column} = ANY(:vals)""")
    with engine.begin() as conn:
        conn.execute(sql, {"vals": list(values)})


def append_daily(engine, schema: str, df: pd.DataFrame):
    if df.empty:
        return
    days = df["transaction_date"].dt.date.unique()
    _delete_rows(engine, schema, "evo_daily_transactions", "transaction_date", days)
    df.to_sql("evo_daily_transactions", engine, schema=schema, if_exists="append", index=False)


def append_monthly(engine, schema: str, df: pd.DataFrame):
    if df.empty:
        return
    keys = df[["year", "month"]].drop_duplicates()
    periods = [f"{int(r.year)}-{int(r.month)}" for _, r in keys.iterrows()]
    _delete_rows(engine, schema, "evo_monthly_transactions", "period_key", periods)
    df["period_key"] = df["year"].astype(str) + "-" + df["month"].astype(str)
    df.to_sql("evo_monthly_transactions", engine, schema=schema, if_exists="append", index=False)


def append_yoy(engine, schema: str, df: pd.DataFrame):
    if df.empty:
        return
    years = df["year"].unique()
    _delete_rows(engine, schema, "evo_yoy_transactions", "year", years)
    df.to_sql("evo_yoy_transactions", engine, schema=schema, if_exists="append", index=False)


def append_kpis(engine, schema: str, df: Dict[str, float], snapshot: date):
    df_out = pd.DataFrame([{**df, "snapshot_date": snapshot}])
    _delete_rows(engine, schema, "evo_global_kpis", "snapshot_date", [snapshot])
    df_out.to_sql("evo_global_kpis", engine, schema=schema, if_exists="append", index=False)


# ======================================================
# MAIN EXECUTION LOGIC (SHORT)
# ======================================================

def run_full_evolution(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    engine = get_engine()
    schema = _get_schema(INSTITUTION_A_CONFIG, "bank_beta_analytics")

    df = load_transactions(engine, start_date, end_date)

    daily = calculate_daily_aggregations(df)
    monthly = calculate_monthly_evolution(df)
    yoy = calculate_yoy_comparison(df)
    kpis = calculate_global_kpis(df)

    append_daily(engine, schema, daily)
    append_monthly(engine, schema, monthly)
    append_yoy(engine, schema, yoy)
    append_kpis(engine, schema, kpis, end_date or date.today())

    return daily, monthly, yoy, kpis
