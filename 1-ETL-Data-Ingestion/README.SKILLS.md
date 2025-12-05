**1 - ETL Data Ingestion — Skills & Highlights**

- **Objetivo:** Ingesta confiable y reproducible de datos desde APIs, archivos y S3 hacia un datalake en Parquet.

- **Habilidades demostradas:**
  - Diseño de pipelines ETL idempotentes y tolerantes a fallos.
  - Trabajo con formatos columnar (Parquet) y optimización de I/O.
  - Manejo de AWS S3 (lectura/escritura), paginación de APIs, y descarga incremental.
  - Uso de `pandas`, `pyarrow` y técnicas de chunking para grandes volúmenes.
  - Implementación de retries y backoff (tenacity / retry utils).
  - Registro estructurado y trazabilidad (rotating logs, correlation ids).

- **Tecnologías:** Python, pandas, pyarrow, boto3, requests, tenacity, pytest (tests sugeridos).

- **Qué contiene el proyecto (puntos clave para mostrar):**
  - Código que extrae datos de fuentes (APIs / S3 / CSV) y normaliza a un esquema común.
  - Transformaciones ligeras para limpieza y tipado antes de escribir Parquet.
  - Utilidades para safe-read/write y para copiar datos a Postgres (batch COPY pattern).

- **Cómo demostrarlo en una entrevista (demo rápido):**
  1. Explicar el flujo: origen → transformaciones → datalake Parquet → DWH load.
  2. Ejecutar una pequeña muestra (ej. `python -c "from commons.data_transforms import safe_read_parquet; print('OK')"`).
  3. Mostrar logs de una corrida local y explicar manejo de errores/retries.

- **Comandos útiles (local/demo):**
  - Crear entorno e instalar deps:
    `python -m venv .venv ; .\.venv\Scripts\Activate ; pip install -r requirements.txt`
  - Ejecutar una tarea de ingesta de ejemplo (modifica para apuntar a datos de prueba):
    `python scripts/run_ingest_example.py --config examples/institution_a_config.py`

- **Puntos fuertes para resaltar en el CV:**
  - Robustez ante fallos: retries, checkpoints y logs.
  - Enfoque en reproducibilidad: configuración por tenant y uso de Parquet para compatibilidad analítica.

- **Siguientes pasos recomendados:** añadir notebooks demo con muestras de datos anonimizadas y tests unitarios para transformaciones.
