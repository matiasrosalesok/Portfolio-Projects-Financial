**2 - Data Warehouse & Transform — Skills & Highlights**

- **Objetivo:** Modelado y carga de datos transformados desde el datalake al esquema del DWH, optimizado para consultas analíticas y reporting.

- **Habilidades demostradas:**
  - Diseño de esquemas DWH (star/snowflake simplificado) y mapeo de entidades.
  - Preparación de datos para cargas masivas (COPY, batching) y manejo de constraints/indexes.
  - Automatización de cargas y despliegue de pre/post-scripts SQL.
  - Validación de integridad y estrategias de backfill/incremental loads.

- **Tecnologías:** PostgreSQL, SQL (optimización), SQLAlchemy, psycopg2, pandas, pytest.

- **Qué contiene el proyecto (puntos clave para mostrar):**
  - Scripts de mapeo DATALAKE → DWH y loader con COPY/transactional patterns.
  - Utilities para normalizar tipos y limpiar datos antes de insertar.
  - Ejemplos de transformaciones 'evolutivos' (agregaciones, series temporales).

- **Demo de entrevista (sugerencia):**
  1. Mostrar el diagrama del modelo DWH y explicar decisiones de column types y particionado.
  2. Ejecutar un loader con dataset reducido y mostrar tiempos/plan de ejecución (EXPLAIN ANALYZE).
  3. Indicar cómo enlazar el DWH con BI (ej. PowerBI) y optimizaciones aplicadas.

- **Comandos útiles (local/demo):**
  - Ejecutar loader (con DB de prueba): `python Warehouse/dwh_loader_uag.py --config tests/config_local.yaml`
  - Ejecutar SQL de ejemplo en psql: `psql postgresql://user:pass@localhost:5432/db -f scripts/sample_load.sql`

- **Puntos fuertes para resaltar en el CV:**
  - Experiencia en carga masiva y modelado para consultas analíticas.
  - Capacidad para balancear rendimiento vs. legibilidad y mantenibilidad.

- **Siguientes pasos:** agregar un conjunto de pruebas de integración que ejecuten un ciclo completo (ingest → transform → carga) usando datos sintéticos.
