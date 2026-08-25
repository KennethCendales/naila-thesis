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

## Tabla de esfuerzo de integración (Día 25)

| Sistema | Versión | Horas documentadas | Componentes afectados | SLOC |
|---|---|---|---|---|
| osCommerce | NAILA | ~3.5h* | 2 | 174 |
| osCommerce | Ad hoc | ~1-1.5h | 1 | 115 |
| Trac | NAILA | ~1.5-2h** | 2 | 176 |
| Trac | Ad hoc | ~1h | 1 | 118 |

*Incluye ~2h del Día 14, que mezclan instalación de Ollama (infraestructura compartida, no específica de osCommerce/NAILA) con la implementación real — imprecisión declarada, no separada en su momento por falta de cronometraje granular.
**Estimado a partir de dos días documentados como "<1 hora" cada uno, sin precisión de minutos.

## Trade-off central identificado (Días 24-25)

**NAILA requiere más esfuerzo de implementación inicial que ad hoc, en ambos casos de estudio — pero produce menor complejidad ciclomática promedio por unidad (Día 24).** Este es precisamente el trade-off que la tesis debe cuantificar y discutir: el costo adicional de diseño arquitectónico (tiempo, más archivos, más LOC total) frente a la ganancia en mantenibilidad estructural. Ninguno de los dos resultados debe presentarse de forma aislada — juntos cuentan la historia completa y honesta del experimento.

## Limitaciones metodológicas de esta medición (a declarar en la tesis)

1. Las horas fueron auto-reportadas en bloques aproximados al final de cada día, no cronometradas con precisión de minutos — esto introduce imprecisión inherente en la métrica de "esfuerzo".
2. El Día 14 mezcla tiempo de infraestructura compartida (instalación de Ollama) con implementación específica — no se puede separar retroactivamente con exactitud.
3. Un solo desarrollador (el investigador) implementó ambas versiones, lo cual introduce un posible efecto de aprendizaje: implementar la segunda versión de un caso de estudio (independientemente de si es NAILA o ad hoc) pudo beneficiarse de familiaridad previa con el dominio de datos, sesgando el tiempo hacia abajo en la segunda implementación de cada sistema.

---

# Cierre de Fase 4 — Resumen consolidado de todas las métricas

## Rendimiento (Día 23)
- Nivel 1 (capa de integración, sin LLM): osCommerce 12-32ms, Trac <1-10ms
- Nivel 2 (end-to-end, con LLM): ~5-7 segundos en todos los escenarios, dominado por la inferencia del modelo

## Mantenibilidad (Día 24)
- Complejidad ciclomática promedio por unidad: NAILA menor que ad hoc en ambos casos de estudio (osCommerce: 1.56 vs. 2.00; Trac: 2.22 vs. 3.25)
- CBO: no comparable directamente entre NAILA (2 y 1) y ad hoc (N/A, sin clases) — la comparación de acoplamiento aplica solo dentro de NAILA

## Esfuerzo de integración (Día 25)
- NAILA requiere más horas y más SLOC total que ad hoc, en ambos casos de estudio

**Fase 4: instrumentación de métricas completa.** Los datos recolectados hasta ahora son de una primera ejecución (n=1 por escenario) — la Fase 5 debe definir si se requieren ejecuciones repetidas para robustez estadística, especialmente dada la variabilidad del LLM ya documentada (Días 17, 23).

