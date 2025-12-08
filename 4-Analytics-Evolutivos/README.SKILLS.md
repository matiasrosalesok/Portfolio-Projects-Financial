**4 - Analytics: Evolutivos — Skills & Highlights**

- **Objetivo:** Desarrollo de pipelines analíticos y métricas evolutivas para seguimiento temporal (ej. evolución de infraestructuras, docentes, grupos).

- **Habilidades demostradas:**
  - Diseño de métricas temporales y series históricas.
  - Agregaciones eficientes y materialized views para reporting.
  - Preparación de datasets para visualización y análisis (PowerBI / Excel / Notebooks).

- **Tecnologías:** Python, pandas, SQL (window functions), PowerBI (modelo conceptual), Jupyter notebooks.

- **Qué contiene el proyecto (puntos clave para mostrar):**
  - Scripts de cálculo de indicadores históricos y pipelines que generan datasets listos para BI.
  - Notebooks explicativos que reproducen los cálculos sobre una muestra de datos.

- **Demo de entrevista (sugerencia):**
  1. Mostrar un notebook con la ejecución paso a paso de una métrica evolutiva.
  2. Explicar cómo se gestionan las ventanas temporales, imputaciones y outliers.

- **Comandos útiles (local/demo):**
  - Abrir notebook demo: `jupyter notebook notebooks/evolutivos_demo.ipynb`
  - Generar dataset de ejemplo: `python evolutivos/generate_sample_dataset.py --out sample.parquet`

- **Puntos fuertes para resaltar en el CV:**
  - Experiencia en transformar datos operacionales en métricas de negocio accionables.

- **Siguientes pasos:** conectar el notebook a un dataset en la nube y mostrar un dashboard embebido (PowerBI/Plotly).
