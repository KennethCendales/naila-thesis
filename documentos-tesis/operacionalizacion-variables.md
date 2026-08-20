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

**Justificación (agregada Día 8, Fase 1):** Siguiendo la recomendación de la literatura revisada (`estado-del-arte.md`, entrada #13), todas las cifras de latencia/rendimiento reportadas en la tesis deben ir acompañadas de las especificaciones del hardware de prueba, y presentarse como resultados relativos/comparativos entre NAILA y el baseline ad hoc, no como cifras universales generalizables a cualquier infraestructura.

**Hardware de prueba (confirmado Día 12):**

| Componente | Especificación |
|---|---|
| Equipo | PC de sobremesa (DESKTOP-134FTGN) |
| Procesador | AMD Ryzen 7 5700G con gráficos Radeon (3.80 GHz) |
| RAM | 48.0 GB instalados (47.8 GB utilizables) |
| GPU | NVIDIA GeForce RTX 3060 (8 GB) |
| Almacenamiento | 477 GB total (213 GB en uso al momento de la prueba) |
| Sistema operativo | Windows, 64 bits, procesador x64 |

Esta tabla debe incluirse tal cual (o resumida) en la sección de metodología/diseño experimental de la tesis, como parte de las condiciones de reproducibilidad del experimento.

---

---

## Definición operacional de "capa de integración" (Día 12, Fase 2)

### Qué SÍ cuenta como capa de integración (unidad de medición del Nivel 1)

- Todo el código fuente escrito por el investigador que implementa el **Adapter/API Facade** y la **Anti-Corruption Layer**, para cada versión (NAILA y ad hoc), en cada caso de estudio.
- Debe implementarse como **código orientado a objetos**, independientemente de si el sistema legacy subyacente es procedural (osCommerce) u orientado a objetos (Trac) — esto garantiza que CBO y complejidad ciclomática sean comparables entre ambos casos de estudio, ya que se miden siempre sobre código propio con el mismo estilo, no sobre el estilo heterogéneo de cada legacy.
- Incluye: clases adaptadoras, clases de traducción/mapeo de datos, contratos de intención estructurada (schemas/DTOs), manejo de errores específico de la integración.

### Qué NO cuenta como capa de integración

- El código del **Agente LLM** en sí (orquestación del modelo de lenguaje, prompts, lógica de function calling) — se considera una capa distinta, no medida en el Nivel 1.
- El código **original del sistema legacy** (osCommerce, Trac) — permanece sin modificar por definición del proyecto, y no se mide como parte de la intervención.
- Scripts de infraestructura (Dockerfiles, docker-compose.yml) — son configuración de entorno, no código de la arquitectura evaluada.
- **Scripts de prueba/validación (`test_flujo_*.py` y equivalentes)** — (aclarado Día 21) estos archivos ejercitan la capa de integración, pero no son parte de ella. Incluirlos en las métricas de CBO/complejidad/LOC distorsionaría la comparación, ya que ambas versiones (NAILA y ad hoc) requieren un arnés de prueba de complejidad similar, lo cual diluiría artificialmente la diferencia arquitectónica real entre ambas. **Se excluyen explícitamente del Nivel 1.**

### Inventario de archivos medibles (Nivel 1) — actualizado Día 21

| Caso de estudio | Versión | Archivos medibles (producción) | Archivos excluidos (pruebas) |
|---|---|---|---|
| osCommerce | NAILA | `oscommerce_acl.py`, `oscommerce_adapter.py` | `test_flujo_completo.py` |
| osCommerce | Ad hoc | `integracion_adhoc.py` | `test_flujo_adhoc.py` |
| Trac | NAILA | `trac_acl.py`, `trac_adapter.py` | `test_flujo_trac.py` |
| Trac | Ad hoc | `integracion_adhoc_trac.py` | `test_flujo_adhoc_trac.py` |

### Convención de organización de código (para la Fase 3)

Para mantener la definición aplicable de forma idéntica en ambos casos de estudio, cada caso tendrá dos carpetas de integración paralelas:

```
casos-estudio/oscommerce/
├── integracion-naila/      ← Adapter + ACL (arquitectura propuesta)
└── integracion-adhoc/      ← integración mínima viable sin patrón (baseline)

casos-estudio/trac/
├── integracion-naila/
└── integracion-adhoc/
```

Todo archivo dentro de `integracion-naila/` o `integracion-adhoc/` es, por definición, parte de la capa de integración medida. Nada fuera de esas carpetas se considera parte de la intervención.

### Definición de "componente afectado" (pendiente resuelto)

**Unidad de medición: archivo.** Un "componente afectado" se define como un archivo de código fuente dentro de `integracion-naila/` o `integracion-adhoc/` que fue creado o modificado durante la implementación de esa versión. Se eligió "archivo" (no "clase" ni "módulo") como unidad porque es la unidad más consistente de contar entre PHP y Python sin ambigüedad adicional de qué constituye un "módulo" en cada lenguaje.

## Pendiente por definir

_(sin pendientes abiertos por ahora)_

