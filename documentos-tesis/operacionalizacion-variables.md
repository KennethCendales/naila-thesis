# Operacionalización de Variables — NAILA

> Este documento define con precisión cómo se mide cada variable de la tesis, para asegurar consistencia entre los dos casos de estudio (osCommerce y Trac) y evitar ambigüedad al momento de instrumentar (Fase 4 del plan de trabajo).

---

## Diseño de dos niveles de medición

- **Nivel 1 (principal):** capa de integración — arquitectura NAILA vs. integración ad hoc mínima viable.
- **Nivel 2 (secundario):** sistema completo — percepción del usuario final, antes/después.

---

## Tabla de métricas

| Variable | Métrica | Nivel | Fuente | Definición operacional |
|---|---|---|---|---|
| Mantenibilidad | CBO (acoplamiento) | 1 | Chidamber & Kemerer (1994), suite CK | Calculado sobre las clases/módulos que conforman la capa de integración (adaptador + ACL), no sobre el sistema legacy completo |
| Mantenibilidad | Complejidad ciclomática | 1 | McCabe (1976) | Calculado sobre la misma capa de integración |
| Mantenibilidad | LOC modificadas | 1 | Operacionalización propia | Líneas de código añadidas/modificadas para construir la capa de integración en cada versión (NAILA vs. ad hoc) |
| Mantenibilidad | Componentes afectados | 1 | Operacionalización propia | Número de archivos/clases distintos tocados para implementar la integración — pendiente definir unidad exacta de "componente" (archivo vs. clase vs. módulo) |
| Mantenibilidad | Esfuerzo de integración | 1 | Operacionalización propia (declarada como limitación metodológica, sin estándar único en la literatura) | Horas de desarrollo invertidas en construir cada versión de la capa de integración |
| Eficiencia de desempeño | Latencia | 1 y 2 | ISO/IEC 25010 (*Time Behaviour*) + benchmarking | **(Actualizado Día 8)** En el Nivel 1, medir el tiempo entre "el adaptador recibe la intención estructurada" y "el adaptador entrega el resultado traducido desde el sistema legacy" — **excluyendo explícitamente el tiempo de inferencia del LLM**, ya que ese tiempo no es parte de la contribución arquitectónica evaluada. En el Nivel 2, medir latencia end-to-end percibida por el usuario (incluye inferencia del LLM), ya que ahí sí es relevante la experiencia completa |
| Eficiencia de desempeño | Throughput | 2 | ISO/IEC 25010 (*Capacity*) | Medido a nivel de sistema completo (Nivel 2) |
| Eficiencia de desempeño | Uso de CPU/RAM | 2 | ISO/IEC 25010 (*Resource Utilization*) | Medido a nivel de sistema completo (Nivel 2) |

---

## Nota metodológica — exclusión del tiempo de inferencia del LLM

**Justificación (agregada Día 8, Fase 1):** Esta decisión se fundamenta en precedente metodológico de literatura reciente (2026) sobre arquitecturas por capas en sistemas con LLM, donde se excluye consistentemente el tiempo de inferencia del modelo al medir el overhead atribuible al framework/capa evaluada, ya que ese tiempo depende del proveedor del modelo y de la infraestructura, no del diseño arquitectónico bajo estudio. Ver `estado-del-arte.md`, entradas #13 y #14, para las fuentes específicas.

**Implicación práctica para la Fase 4 (instrumentación):** El código de la capa de integración deberá registrar explícitamente dos marcas de tiempo:
1. Timestamp al recibir la intención ya estructurada (después de que el LLM procesó el lenguaje natural, pero antes de que el adaptador actúe)
2. Timestamp al entregar el resultado traducido desde el sistema legacy

La diferencia entre ambos es la métrica de latencia del Nivel 1. La latencia total end-to-end (incluyendo el LLM) se mide por separado para el Nivel 2.

---

## Nota metodológica — limitaciones de hardware

**Justificación (agregada Día 8, Fase 1):** Siguiendo la recomendación de la literatura revisada (`estado-del-arte.md`, entrada #13), todas las cifras de latencia/rendimiento reportadas en la tesis deben ir acompañadas de las especificaciones del hardware de prueba (laptop HP OMEN 16 — pendiente documentar specs exactas: CPU, RAM, GPU si aplica), y presentarse como resultados relativos/comparativos entre NAILA y el baseline ad hoc, no como cifras universales generalizables a cualquier infraestructura.

---

## Pendiente por definir

- Definición exacta de "componente afectado" (¿archivo, clase o módulo?) — anotado desde la sesión de definición del nivel de medición, aún sin resolver formalmente.
- Documentar specs exactas del hardware de prueba (HP OMEN 16) antes de la Fase 4.
