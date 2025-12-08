**5 - PowerBI Dashboards — Skills & Highlights**

- **Objetivo:** Preparar datasets y ejemplos de dashboards orientados a usuarios de negocio (KPIs, filtros, tiempos).

- **Habilidades demostradas:**
  - Preparación de modelos tabulares para PowerBI (relaciones, medidas DAX sugeridas).
  - Diseño de dashboards claros: KPI cards, tendencias, segmentación por tenant/periodo.
  - Exportar datasets listos para consumo por herramientas de BI.

- **Tecnologías:** PowerBI (conceptual), Parquet/CSV datasets, pandas para shaping, DAX (sugerencias).

- **Qué contiene el proyecto (puntos clave para mostrar):**
  - Archivos `sample_dashboard_description.md` que detallan el diseño del dashboard y las medidas clave.
  - Scripts para exportar datasets preparados para PowerBI (parquet/csv).

- **Demo de entrevista (sugerencia):**
  1. Presentar un prototipo de dashboard (capturas o PowerBI Desktop si lo tienes).
  2. Explicar decisiones de modelado (columnas duplicadas, joins, granularidad temporal).

- **Comandos útiles (local/demo):**
  - Generar CSV de muestra: `python scripts/export_powerbi_dataset.py --out powerbi_sample.csv`

- **Puntos fuertes para resaltar en el CV:**
  - Capacidad para llevar datos desde el datalake hasta un diseño visual que resuelva preguntas de negocio.

- **Siguientes pasos:** incluir pantallazos del PowerBI o un archivo `.pbix` minimal (si quieres publicar, ten cuidado con datos sensibles).
