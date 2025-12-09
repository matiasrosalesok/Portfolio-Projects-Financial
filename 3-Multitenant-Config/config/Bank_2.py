# config/uax.py (copied for Multitenant demo)
import os
from .base import PG_CONFIG_BASE, REGION

INSTITUTION_A_CONFIG = {
    "CODE": "Bank_2",
    "INSTITUTION_NAME": "Institución Financiera B",
    "DESCRIPTION": "Sistema de datos para procesamiento de transacciones financieras",
    
    # AWS Credentials
    "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY_INST_B"),
    "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY_INST_B"),
    "AWS_ACCESS_KEY_SAND": os.getenv("AWS_ACCESS_KEY_SAND_B"),
    "AWS_SECRET_KEY_SAND": os.getenv("AWS_SECRET_KEY_SAND_B"),
    "REGION": "us-east-1",
    
    # API Pipeline Configuration
    "TOKEN": "01318bd7d83de8df17dd52330a8e5e6be0b75b91",
    "PIPELINE_CODE": "financial/data/ingestion/by_source",
    "API_URL_BASE": "https://institution-b.api.data-platform.com",
    "TENANT_SUBDOMAIN": "institution-b",
    "CLIENT_ID": "institution_b",
    
    # Data Sources
    "EXTENSION_A_DESCARGAR": ".parquet",
    "LOCAL_FOLDER": r"C:\DataSources\Institution_B",
    "DATA_ENTITIES": [
        "transactions_data",
        "account_holders",
        "financial_products",
        "transaction_channels",
        "account_balances",
        "transaction_details",
        "account_categories"
    ],
    
    # Database Configuration
    "DB_SCHEMA": "institution_b",
    "TABLE_MASTER": '"institution_b"."control_context"',
    "DATALAKE_TABLE": '"institution_b".raw_data_parquet',
    
    # Data Warehouse Mapping
    "DWH_SCHEMA": "institution_a_dw",
    "TABLE_MAPPING": {
        "financial_products": "std_financial_products",
        "account_holders": "std_account_holders",
        "transactions_data": "std_transactions",
        "transaction_channels": "std_transaction_channels",
        "account_balances": "std_account_balances",
        "transaction_details": "std_transaction_details",
        "account_categories": "std_account_categories"
    },
    
    # Performance Settings
    "BATCH_SIZE": 50000,
    "MAX_CONNECTIONS": 5,
    "TIMEOUT_SECONDS": 300
}