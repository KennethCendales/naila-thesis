# Resultados — NAILA

> Redactado en tercera persona/pasiva, tono académico. Presenta los hallazgos sin interpretarlos en profundidad (eso corresponde a la sección de Discusión, Día 28). Referencia directa a `resultados-mantenibilidad.md` y `resultados-experimento-comparativo.md` para las tablas completas de datos crudos.

## 1. Resultados de mantenibilidad

Se calculó el acoplamiento entre objetos (CBO) y la complejidad ciclomática sobre los archivos de producción de la capa de integración en ambos casos de estudio, para las versiones NAILA y ad hoc.

En cuanto a CBO, la versión NAILA de osCommerce presentó valores de 2 (OsCommerceACL) y 1 (OsCommerceAdapter); la versión NAILA de Trac presentó valores de 1 (TracACL) y 1 (TracAdapter). Dado que las versiones ad hoc no implementan clases (por diseño experimental, ver Día 17/20), la métrica de CBO no es aplicable a esa versión, por lo que la comparación de acoplamiento se circunscribe a un análisis interno de la arquitectura NAILA.

En cuanto a complejidad ciclomática, se calculó el promedio por unidad (método o función) en cada versión. Los resultados muestran que la arquitectura NAILA presenta menor complejidad ciclomática promedio que la versión ad hoc en ambos casos de estudio: en osCommerce, 1.56 (NAILA, n=9 unidades) frente a 2.00 (ad hoc, n=4 unidades); en Trac, 2.22 (NAILA, n=9 unidades) frente a 3.25 (ad hoc, n=4 unidades). Esto representa una reducción del 22% y 32% respectivamente.

En cuanto a líneas de código fuente (SLOC), la versión NAILA requirió más líneas de código totales, distribuidas en dos archivos, que la versión ad hoc, concentrada en un solo archivo: en osCommerce, 174 SLOC (NAILA, 2 archivos) frente a 115 SLOC (ad hoc, 1 archivo); en Trac, 176 SLOC (NAILA, 2 archivos) frente a 118 SLOC (ad hoc, 1 archivo).

## 2. Resultados de esfuerzo de integración

El esfuerzo de integración, medido en horas de desarrollo documentadas y número de componentes (archivos) afectados, fue consistentemente mayor para la versión NAILA en ambos casos de estudio. En osCommerce, la implementación de NAILA requirió aproximadamente 3.5 horas frente a 1-1.5 horas de la versión ad hoc. En Trac, NAILA requirió aproximadamente 1.5-2 horas frente a 1 hora de la versión ad hoc. En ambos casos, NAILA afectó 2 componentes (archivos) frente a 1 componente de la versión ad hoc.

Se declara como limitación metodológica que estas mediciones de tiempo fueron auto-reportadas en bloques aproximados al final de cada sesión de trabajo, no cronometradas con precisión de minutos, y que la medición del primer caso de estudio (osCommerce, Día 14) incluye tiempo de instalación de infraestructura compartida (el motor de inferencia local) no separable retroactivamente del tiempo de implementación específico.

## 3. Resultados de eficiencia de desempeño

Se ejecutaron 120 mediciones (10 repeticiones × 3 casos de uso × 4 escenarios), con parámetros de cantidad fijados explícitamente en las solicitudes del usuario para controlar la variabilidad no determinista observada en el comportamiento del modelo de lenguaje durante las fases previas del proyecto.

**Nivel 1 (capa de integración, excluyendo la inferencia del modelo de lenguaje):** la versión ad hoc presentó menor latencia promedio que NAILA en ambos casos de estudio. En osCommerce, la media de ad hoc fue de 18.10 ms (desviación estándar = 8.66) frente a 23.17 ms (desviación estándar = 10.09) de NAILA. En Trac, la media de ad hoc fue de 0.86 ms (desviación estándar = 0.10) frente a 0.85-1.16 ms de NAILA, dependiendo de si se excluye un valor atípico de arranque en frío registrado en la primera repetición.

**Nivel 2 (sistema completo, incluyendo la inferencia del modelo de lenguaje):** no se observaron diferencias sustanciales entre NAILA y ad hoc en ninguno de los dos casos de estudio. En osCommerce, las medias fueron de 5335.72 ms (NAILA) y 5400.89 ms (ad hoc). En Trac, las medias fueron de 5532.12 ms (NAILA) y 5471.13 ms (ad hoc). En ambos casos, la diferencia entre versiones fue considerablemente menor que la desviación estándar observada (aproximadamente 600-670 ms en todos los escenarios).

**Comparación entre casos de estudio:** independientemente de la versión evaluada, Trac presentó latencias de Nivel 1 entre 15 y 20 veces menores que osCommerce, atribuible al mecanismo de persistencia de cada sistema legacy (acceso directo a archivo SQLite en Trac frente a conexión de red a un servidor MySQL en osCommerce).

## 4. Síntesis de resultados por dimensión

| Dimensión | Resultado observado |
|---|---|
| Complejidad ciclomática promedio | NAILA menor en ambos casos de estudio |
| Acoplamiento (CBO) | No comparable directamente con ad hoc (sin clases); NAILA presenta acoplamiento bajo (1-2) |
| Esfuerzo de integración (horas, componentes) | NAILA mayor en ambos casos de estudio |
| Latencia Nivel 1 | Ad hoc menor en ambos casos de estudio |
| Latencia Nivel 2 | Sin diferencia estadísticamente distinguible |

Estos resultados se interpretan y se contrastan con la literatura revisada en la sección de Discusión (Día 28).
