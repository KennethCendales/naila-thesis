# Resultados del Experimento Comparativo — NAILA (Fase 5)

> Medición formal: 10 repeticiones × 3 casos de uso × 4 escenarios = 120 mediciones totales. Parámetros de cantidad fijados explícitamente en los mensajes de usuario para controlar la variabilidad no determinista del LLM documentada en las Fases 3-4.

## Tabla de resultados (media ± desviación estándar, n=30 por escenario)

| Escenario | Nivel 1 (ms) | Nivel 2 (ms) |
|---|---|---|
| osCommerce — NAILA | 23.17 ± 10.09 | 5335.72 ± 667.29 |
| osCommerce — Ad hoc | 18.10 ± 8.66 | 5400.89 ± 672.94 |
| Trac — NAILA | 1.16 ± 1.74 (0.85 ± 0.05 excluyendo outlier de arranque en frío) | 5532.12 ± 629.06 |
| Trac — Ad hoc | 0.86 ± 0.10 | 5471.13 ± 597.39 |

## Hallazgo principal — Nivel 1: ad hoc es más rápido que NAILA en ambos casos de estudio

**Este resultado no refuta la tesis — la enriquece con un trade-off honesto.** La versión ad hoc es consistentemente más rápida en el Nivel 1 en ambos casos de estudio (osCommerce: ~5ms de diferencia promedio; Trac: diferencia marginal, casi nula al excluir el outlier). Esto es coherente con la teoría de arquitectura de software: la separación de responsabilidades (Adapter → ACL) introduce una capa adicional de indirección (una llamada a método extra) frente a una función plana que resuelve todo directamente — el costo de rendimiento clásico y esperado de la abstracción arquitectónica.

**Interpretación para la discusión de resultados:** NAILA sacrifica una pequeña cantidad de rendimiento en la capa de integración a cambio de mejor mantenibilidad (menor complejidad ciclomática promedio, Día 24). Este es el trade-off central que la tesis debe cuantificar y discutir explícitamente — no se trata de que "NAILA sea mejor en todo", sino de que ofrece una relación costo-beneficio distinta y potencialmente más favorable a largo plazo (mantenibilidad) a cambio de un costo marginal y consistente en el corto plazo (rendimiento, esfuerzo de implementación).

## Nivel 2 — sin diferencias significativas entre NAILA y ad hoc

Las medias de Nivel 2 son muy cercanas entre NAILA y ad hoc en ambos casos de estudio (diferencias de 1-2% del valor total), y las desviaciones estándar (~600-670ms) son mucho mayores que la diferencia entre versiones — es decir, **la diferencia entre NAILA y ad hoc en Nivel 2 no es distinguible del ruido de la inferencia del LLM.** Esto confirma, con datos formales, la decisión metodológica del Día 8: el Nivel 2 está dominado por un factor externo (el LLM) que no es parte de la contribución arquitectónica evaluada, razón por la cual el Nivel 1 es la métrica de rendimiento verdaderamente relevante para esta tesis.

## Nota metodológica — outlier de arranque en frío en Trac NAILA

La primera repetición de `list_open_tickets` en Trac NAILA registró 10.359 ms, muy por encima del resto de la distribución (0.75-0.95 ms) — consistente con el costo de abrir la primera conexión al archivo SQLite (buffers de caché de archivo aún no calientes). Se reporta tanto el resultado con el outlier incluido (fiel a los datos crudos) como excluyéndolo (más representativo del comportamiento en estado estable), siguiendo buena práctica de transparencia metodológica: declarar el tratamiento de outliers explícitamente, no ocultarlo.

## Diferencia entre casos de estudio — SQLite vs. MySQL

Se confirma con datos estadísticos robustos (no solo la primera corrida piloto) el hallazgo del Día 23: **Trac (SQLite) es entre 15-20x más rápido que osCommerce (MySQL) en el Nivel 1**, independientemente de la versión (NAILA o ad hoc). Esto refleja una diferencia real en el mecanismo de persistencia de cada sistema legacy, no una diferencia atribuible a la arquitectura de integración — un hallazgo cualitativo relevante para la discusión, que matiza cualquier generalización sobre "cuánto cuesta" la capa de integración en términos absolutos.

## Resumen consolidado — Fases 4 y 5 juntas

| Dimensión | Resultado |
|---|---|
| Complejidad ciclomática promedio (Día 24) | NAILA menor en ambos casos de estudio (mejor mantenibilidad) |
| Esfuerzo de integración (Día 25) | NAILA requiere más horas y SLOC en ambos casos de estudio (mayor costo inicial) |
| Latencia Nivel 1 (Día 26) | Ad hoc más rápido en ambos casos de estudio (menor overhead de indirección) |
| Latencia Nivel 2 (Día 26) | Sin diferencia significativa (dominado por el LLM) |

**Síntesis para la tesis:** NAILA presenta un trade-off claro y cuantificado: mejor mantenibilidad estructural a cambio de mayor esfuerzo de implementación y un costo marginal de rendimiento en la capa de integración. Ninguna de las dos versiones es objetivamente "mejor" en todas las dimensiones — la contribución de la tesis es precisamente cuantificar este trade-off con evidencia empírica, permitiendo que futuros equipos de desarrollo tomen esta decisión de forma informada según sus prioridades (mantenibilidad a largo plazo vs. velocidad de entrega y rendimiento marginal).

---

# Prueba de significancia estadística (t de Welch) — actualización posterior a la Fase 6

> Aplicada como parte del trabajo de fortalecimiento de la tesis, siguiendo la línea de trabajo futuro de corto plazo ya identificada (`conclusiones-trabajo-futuro.md`, punto 1). Se usa la prueba t de Welch (no asume varianzas iguales entre grupos), apropiada dado que ya se había observado variabilidad muy distinta entre osCommerce y Trac.

## Resultados

| Comparación | Media NAILA | Media Ad hoc | t | p | Significativo (α=0.05) |
|---|---|---|---|---|---|
| osCommerce — Nivel 1 | 23.17 ms | 18.10 ms | 2.087 | 0.0414 | **Sí** |
| osCommerce — Nivel 2 | 5335.72 ms | 5400.89 ms | -0.377 | 0.7078 | No |
| Trac — Nivel 1 (con outlier) | 1.16 ms | 0.86 ms | 0.948 | 0.3510 | No |
| Trac — Nivel 1 (sin outlier) | 0.85 ms | 0.86 ms | -0.798 | 0.4287 | No |
| Trac — Nivel 2 | 5532.12 ms | 5471.13 ms | 0.385 | 0.7016 | No |

## Interpretación — matiz importante frente a las secciones previas de Resultados y Discusión

**La diferencia de latencia en Nivel 1 (ad hoc más rápido que NAILA) solo alcanza significancia estadística en osCommerce, no en Trac.** Esto refina — no invalida — el hallazgo original: el costo de rendimiento de la separación arquitectónica (Adapter → ACL) es real y medible cuando la latencia base del sistema legacy es suficientemente alta (osCommerce, con conexión de red a MySQL), pero se diluye en el ruido de medición cuando la latencia base es extremadamente baja (Trac, acceso directo a archivo SQLite, latencias sub-milisegundo).

**Todas las comparaciones de Nivel 2 confirman, ahora con respaldo estadístico formal, lo que ya se argumentaba cualitativamente**: no hay diferencia distinguible entre NAILA y ad hoc a nivel de sistema completo — el ruido de la inferencia del LLM domina por completo cualquier señal arquitectónica.

## Consecuencia para el texto de la tesis

Las secciones `resultados-tesis.md`, `discusion-tesis.md` y `limitaciones-tesis.md` deben actualizarse para reflejar este matiz: el trade-off de rendimiento es real y significativo en al menos un caso de estudio (osCommerce), pero no se generaliza automáticamente a cualquier sistema legacy — depende de la magnitud de la latencia base del sistema, un hallazgo en sí mismo relevante para la guía de generalización de NAILA.
