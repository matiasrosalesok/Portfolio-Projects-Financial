3 - Multitenant Configuration

Resumen
- Plantillas y helpers para gestionar configuración por tenant y aislar secretos.

Habilidades clave
- Diseño de multi-tenant, validación de configs y separación de secretos.

Quick start
1. Copia `.env.example` a `.env` y llena valores locales.
2. Instalar deps: `pip install -r requirements.txt`
3. Validar configs (ejemplo): `python scripts/validate_configs.py --path config/`

Detalles
- Ver `config/` para ejemplos de `ue.py`, `uax.py`, `uag.py` adaptados a variables de entorno.
# ⚙️ Multi-Tenant Configuration System

**Scalable configuration management for multiple financial institutions**

## 🎯 Overview

Centralized configuration system that enables managing multiple independent financial institutions through a single codebase. Each institution has isolated configuration, credentials, and database schemas while sharing common infrastructure.

### Key Benefits
- **Scalability:** Add new institutions without code changes
- **Security:** Isolated credentials per institution
- **Maintainability:** Single source of truth for configuration
- **Flexibility:** Override defaults per institution

---

## 🏗️ Architecture

```
Multi-Tenant Configuration
├── Base Configuration (Common)
│   ├── Database connection
│   ├── AWS region
│   ├── API timeouts
│   └── Logging levels
│
└── Institution-Specific
    ├── Institution A Config
    │   ├── AWS credentials
    │   ├── Schema name
    │   ├── Data entities
    │   └── Table mappings
    │
    ├── Institution B Config
    ├── Institution C Config
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Config Management:** Environment variables + Config files
- **Secrets:** AWS Secrets Manager / .env files
- **Validation:** Pydantic models
- **Documentation:** Type hints + docstrings

---

## ✨ Features

✅ **Centralized Configuration** - Single source of truth  
✅ **Environment-Based Overrides** - dev/staging/production  
✅ **Secure Credential Management** - No hardcoded secrets  
✅ **Institution Isolation** - Each tenant has own schema  
✅ **Dynamic Loading** - Load configs at runtime  
✅ **Validation** - Config schema validation  
✅ **Documentation** - Auto-generated from code  

---

## 📂 Project Structure

```
3-Multitenant-Config/
├── base_config.py
├── institution_a_config.py
├── institution_b_config.py
├── institution_c_config.py
├── config_loader.py
├── config_validator.py
├── examples/
│   ├── .env.example
│   ├── institution_a_example.py
│   └── usage_example.py
└── README.md
```

---

## 📋 Configuration Hierarchy

### 1. Base Configuration (All Institutions)
```python
# base_config.py
REGION = "us-east-1"
LOG_LEVEL = "INFO"
DB_POOL_SIZE = 10
TIMEOUT_SECONDS = 300
BATCH_SIZE = 50000
```

### 2. Institution-Specific Configuration
```python
# institution_a_config.py
INSTITUTION_A_CONFIG = {
    "CODE": "institution_a",
    "NAME": "Financial Institution A",
    
    # Override base settings
    "BATCH_SIZE": 75000,  # Larger batches
    "TIMEOUT_SECONDS": 600,  # Longer timeout
    
    # Institution-specific settings
    "SCHEMA": "institution_a",
    "AWS_BUCKET": "fin-data-inst-a",
    "DATA_ENTITIES": ["transactions", "accounts"],
    "TABLE_MAPPINGS": {...}
}
```

---

## 🚀 Usage Examples

### Load Configuration for Institution

```python
from config_loader import load_institution_config

# Load dynamically
config = load_institution_config("institution_a")

print(config["INSTITUTION_NAME"])
print(config["DB_SCHEMA"])
print(config["DATA_ENTITIES"])
```

### Access Configuration in Code

```python
from institution_a_config import INSTITUTION_A_CONFIG

# Use configuration
db_schema = INSTITUTION_A_CONFIG["DB_SCHEMA"]
s3_bucket = INSTITUTION_A_CONFIG["AWS_BUCKET"]
entities = INSTITUTION_A_CONFIG["DATA_ENTITIES"]

for entity in entities:
    process_entity(entity, db_schema)
```

### Override with Environment Variables

```bash
export INSTITUTION_A_SCHEMA="custom_schema"
export INSTITUTION_A_BATCH_SIZE=100000
export LOG_LEVEL=DEBUG
```

```python
config = load_institution_config("institution_a")
# Will use environment overrides if present
```

---

## 📊 Configuration Structure

Each institution config includes:

```python
INSTITUTION_CONFIG = {
    # Identity
    "CODE": "unique_code",
    "INSTITUTION_NAME": "Display Name",
    "DESCRIPTION": "What this institution does",
    
    # AWS Credentials (from env vars for security)
    "AWS_ACCESS_KEY": os.getenv("AWS_KEY_INST_A"),
    "AWS_SECRET_KEY": os.getenv("AWS_SECRET_INST_A"),
    "REGION": "us-east-1",
    
    # API Configuration
    "TOKEN": "api_token",
    "PIPELINE_CODE": "pipeline/identifier",
    "API_URL_BASE": "https://api.institution-a.com",
    "TENANT_SUBDOMAIN": "institution-a",
    
    # Data Sources
    "DATA_ENTITIES": ["entity1", "entity2", ...],
    "LOCAL_FOLDER": r"C:\Data\Institution_A",
    
    # Database
    "DB_SCHEMA": "institution_a",
    "TABLE_MASTER": '"institution_a"."master"',
    "DATALAKE_TABLE": '"institution_a"."raw_data"',
    
    # Warehouse
    "DWH_SCHEMA": "institution_a_dw",
    "TABLE_MAPPINGS": {
        "source_table": "target_table"
    },
    
    # Performance
    "BATCH_SIZE": 50000,
    "MAX_CONNECTIONS": 5,
    "TIMEOUT_SECONDS": 300
}
```

---

## 🔐 Security Best Practices

### ❌ DON'T DO THIS:
```python
"AWS_ACCESS_KEY": "AKIAIOSFODNN7EXAMPLE",  # Hardcoded!
"AWS_SECRET_KEY": "wJalrXUtnFEMI...",      # Exposed!
```

### ✅ DO THIS:
```python
"AWS_ACCESS_KEY": os.getenv("AWS_KEY_INST_A"),
"AWS_SECRET_KEY": os.getenv("AWS_SECRET_INST_A"),
```

### Setup Environment:
```bash
# .env file (NOT in version control)
AWS_KEY_INST_A=AKIA...
AWS_SECRET_INST_A=wJalr...
AWS_KEY_INST_B=AKIA...
AWS_SECRET_INST_B=wJalr...
```

---

## ➕ Adding New Institution

### Step 1: Create Config File
```python
# institution_d_config.py
INSTITUTION_D_CONFIG = {
    "CODE": "institution_d",
    "INSTITUTION_NAME": "Institution D",
    ...
}
```

### Step 2: Add to Loader
```python
# config_loader.py
AVAILABLE_INSTITUTIONS = {
    "institution_a": INSTITUTION_A_CONFIG,
    "institution_b": INSTITUTION_B_CONFIG,
    "institution_c": INSTITUTION_C_CONFIG,
    "institution_d": INSTITUTION_D_CONFIG,  # Add this
}
```

### Step 3: Update Environment
```bash
# Add credentials to .env
AWS_KEY_INST_D=...
AWS_SECRET_INST_D=...
```

### Step 4: Done! ✓
```python
config = load_institution_config("institution_d")
# No code changes needed in ETL or DW modules
```

---

## 🧪 Configuration Validation

```python
from config_validator import validate_config

# Validate before using
config = load_institution_config("institution_a")
is_valid = validate_config(config)

if not is_valid:
    raise ConfigurationError("Invalid configuration")
```

Validates:
- All required fields present
- Correct data types
- Valid URL formats
- Database connectivity
- AWS credentials validity

---

## 📝 Example: .env File

```bash
# Database (Common)
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=secure_password

# Institution A Credentials
AWS_KEY_INST_A=AKIA...
AWS_SECRET_INST_A=wJalr...
API_TOKEN_A=token_a...

# Institution B Credentials
AWS_KEY_INST_B=AKIA...
AWS_SECRET_INST_B=wJalr...
API_TOKEN_B=token_b...

# Institution C Credentials
AWS_KEY_INST_C=AKIA...
AWS_SECRET_INST_C=wJalr...
API_TOKEN_C=token_c...

# Application Settings
LOG_LEVEL=INFO
ENVIRONMENT=production
```

---

## 💡 What I Learned Building This

1. **Multi-Tenant Architecture** - Design patterns for scalability
2. **Configuration Management** - Centralized vs distributed configs
3. **Secrets Management** - Secure credential handling
4. **Environment Overrides** - Dev/staging/production setups
5. **Validation Patterns** - Config schema validation

---

## 🔧 Maintenance

### Adding New Global Setting
```python
# base_config.py
NEW_GLOBAL_SETTING = "value"

# All institutions automatically inherit
```

### Overriding for One Institution
```python
# institution_a_config.py
INSTITUTION_A_CONFIG = {
    ...
    "NEW_GLOBAL_SETTING": "institution_a_specific_value"  # Override
}
```

---

**Last Updated:** December 2025  
**Status:** Production-Ready ✓  
**Institutions Supported:** 3+

