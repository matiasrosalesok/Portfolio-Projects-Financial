**3 - Multitenant Configuration — Skills & Highlights**

- **Objetivo:** Proveer una configuración escalable y segura para múltiples tenants (instituciones), con posibilidad de desplegar el mismo pipeline por cliente.

- **Habilidades demostradas:**
  - Diseño de configuración por tenant (separación de parámetros y secretos).
  - Uso de patterns para multi-tenancy: configuración por archivo/env, prefijos de esquema, y nombres de tabla dinámicos.
  - Implementación de safeguards para evitar fugas de datos entre tenants.

- **Tecnologías:** Python, .env, YAML/JSON config, pattern-based templating, unit testing de config.

- **Qué contiene el proyecto (puntos clave para mostrar):**
  - Ejemplos de `institution_a_config.py` y plantillas para nuevos tenants.
  - Helpers para resolver settings, validar valores y aplicar transformaciones por tenant.

- **Demo de entrevista (sugerencia):**
  1. Mostrar cómo añadir un nuevo tenant (copia de config + variables) en 2 minutos.
  2. Explicar controles para evitar que un job de un tenant acceda a otro (nombres de esquema, prefijos, roles DB).

- **Comandos útiles (local/demo):**
  - Validar configs: `python scripts/validate_configs.py --path config/` (ejemplo de script utilitario).

- **Puntos fuertes para resaltar en el CV:**
  - Implementación práctica y segura de multi-tenant en pipelines de datos.

- **Siguientes pasos:** escribir pruebas que simulen dos tenants y verifiquen aislamiento de datos.
