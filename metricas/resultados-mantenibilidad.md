# Resultados de Mantenibilidad — NAILA (Día 24, Fase 4)

> Datos preliminares de la primera medición. Se consolidarán con los resultados de esfuerzo de integración (Día 25) y se someterán a análisis estadístico formal en la Fase 6.

## Tabla completa de resultados

| Sistema | Versión | Archivo | Clase/Función | CBO | Complejidad ciclomática (por unidad) | SLOC |
|---|---|---|---|---|---|---|
| osCommerce | NAILA | `oscommerce_acl.py` | OsCommerceACL | 2 | 1, 1, 2, 2, 3 | 96 |
| osCommerce | NAILA | `oscommerce_adapter.py` | OsCommerceAdapter | 1 | 1, 1, 1, 2 | 78 |
| osCommerce | Ad hoc | `integracion_adhoc.py` | (funciones sueltas) | N/A | 1, 2, 2, 3 | 115 |
| Trac | NAILA | `trac_acl.py` | TracACL | 1 | 2, 2, 4, 4, 3 | 98 |
| Trac | NAILA | `trac_adapter.py` | TracAdapter | 1 | 1, 1, 1, 2 | 78 |
| Trac | Ad hoc | `integracion_adhoc_trac.py` | (funciones sueltas) | N/A | 2, 4, 4, 3 | 118 |

*CBO no aplica a las versiones ad hoc por diseño (no usan clases).*

## Métricas derivadas — complejidad ciclomática promedio por unidad

| Sistema | NAILA (2 archivos combinados) | Ad hoc (1 archivo) | Diferencia |
|---|---|---|---|
| osCommerce | 1.56 (n=9) | 2.00 (n=4) | NAILA 22% menor |
| Trac | 2.22 (n=9) | 3.25 (n=4) | NAILA 32% menor |

**Hallazgo preliminar:** en ambos casos de estudio, la arquitectura NAILA presenta menor complejidad ciclomática promedio por unidad que la versión ad hoc — consistente con la hipótesis de que la separación de responsabilidades (Adapter/ACL) distribuye la complejidad en piezas más pequeñas, en vez de concentrarla en funciones monolíticas.

**Nota sobre SLOC:** la versión ad hoc tiene más líneas de código totales en un solo archivo (115-118 SLOC) que cada archivo individual de NAILA, pero menos que la suma de ambos archivos NAILA combinados (174-176 SLOC). Esto es un dato a interpretar con cuidado en la discusión: NAILA "cuesta más" en LOC total, pero distribuye esa complejidad en unidades más pequeñas y con menor complejidad ciclomática promedio — un trade-off real entre cantidad de código y calidad estructural por unidad, que vale la pena discutir explícitamente en los resultados finales.

## Historial de refinamiento del instrumento de medición (CBO)

1. **v1 (Día 22):** detectaba acoplamiento solo en llamadas (`Call`) y anotaciones de tipo (`AnnAssign`) — subestimaba CBO (ej. no detectaba `pymysql.cursors.DictCursor` usado como valor de diccionario).
2. **v2 (Día 22):** rastreo de imports + detección en cualquier contexto — corrigió la subestimación, pero sobreestimaba en casos con manipulación de rutas de archivos (`os.path.*` contado como acoplamiento).
3. **v3 (Día 24):** exclusión de módulos de utilidad genérica del sistema (`os`, `sys`), manteniendo módulos de acceso a datos/persistencia (`sqlite3`, `pymysql`) como acoplamiento válido — versión final usada para estos resultados.

Este proceso de refinamiento iterativo del instrumento de medición es en sí mismo evidencia de rigor metodológico, documentable en la sección de metodología de la tesis.
