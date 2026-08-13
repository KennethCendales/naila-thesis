# NAILA — Resumen Ejecutivo
*Actualizado al cierre de la Fase 1 (Estado del Arte)*

## Título
Arquitectura no invasiva para la integración de agentes de IA generativa en sistemas de software heredados: evaluación empírica de rendimiento y mantenibilidad mediante casos de estudio múltiples

## Objetivo general
Diseñar, implementar y evaluar empíricamente una arquitectura no invasiva que incorpore agentes de IA generativa (LLM) sobre sistemas heredados, midiendo su impacto en eficiencia de desempeño y mantenibilidad (ISO/IEC 25010), frente a un enfoque de integración ad hoc, mediante 2 casos de estudio.

## Decisiones de diseño cerradas
| Aspecto | Decisión |
|---|---|
| Patrón arquitectónico | Anti-Corruption Layer (Evans, 2003) + Adapter (Gamma et al., 1994) |
| Casos de estudio | osCommerce v2.3.4 (PHP) + Trac (Python) — ambos funcionando en Docker |
| Diseño comparativo | NAILA vs. integración ad hoc mínima viable |
| Niveles de medición | Nivel 1: capa de integración (CBO, complejidad ciclomática, LOC, esfuerzo). Nivel 2: sistema completo (latencia, CPU/RAM, throughput) |
| Métrica de latencia (Nivel 1) | Excluye tiempo de inferencia del LLM — aísla el overhead arquitectónico propio |

## Vacío de investigación (resumen)
No existe arquitectura validada empíricamente para integrar agentes LLM como interfaz de interacción sobre sistemas heredados sin modificar su lógica de negocio. La literatura existente o es puramente conceptual (Bucaioni et al., 2025), o resuelve problemas adyacentes (recuperación de arquitectura legacy, colaboración multiagente en desarrollo). Los patrones ACL/Adapter están validados en general, pero no en el dominio específico de agentes de IA generativa.

## Estado de avance práctico
- ✅ **Fase 0 completa:** ambos sistemas legacy corriendo en Docker, repositorio y documentación (bitácora, ADRs, incidentes) al día
- ✅ **Fase 1 completa (Días 6-9):** 15 fuentes académicas documentadas, fundamentación de patrones arquitectónicos y métricas, vacío de investigación consolidado
- ⏳ **Día 10 (en curso):** redacción formal de la justificación
- ⏸️ **Siguiente:** Fase 2 — diseño detallado de la arquitectura NAILA (diagrama de referencia, definición de "capa de integración", selección de modelo LLM, primer prototipo)

## Documentos del proyecto
`bitacora.md` · `decisiones-arquitectonicas.md` (5 ADRs) · `incidentes-tecnicos.md` (4 incidentes) · `estado-del-arte.md` (15 fuentes) · `operacionalizacion-variables.md`
