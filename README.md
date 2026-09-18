# NAILA — Non-Invasive Architecture for Integrating LLM Agents

**Tesis:** Arquitectura no invasiva para la integración de agentes de IA generativa en sistemas de software heredados: evaluación empírica de rendimiento y mantenibilidad mediante casos de estudio múltiples

**Autor:** Kenneth Cendales — Universidad Manuela Beltrán

## Por qué existe esta investigación

El origen de esta investigación no es anecdótico. A nivel global, los sistemas legacy sostienen el 70% de las operaciones críticas de negocio, según datos citados de Hashbyt (2026), y en muchas organizaciones hasta el 75% del gasto tecnológico se destina únicamente a mantenerlos funcionando, sin poder invertir en evolucionarlos. En Colombia, el propio Ministerio TIC reconoce la infraestructura tecnológica obsoleta como una barrera institucional para la transformación digital en su Marco de la Transformación Digital para el Estado Colombiano, y estudios empíricos en universidades colombianas —incluyendo encuestas directas a pymes— documentan esa misma limitación como un obstáculo real y medido, no supuesto. Ese es el problema documentado del que parte NAILA: reemplazar un sistema legacy es costoso y riesgoso, una realidad reconocida institucional y académicamente, no descubierta por intuición personal.

La valía de esta tesis no está en construir un chat con IA —esa es una capacidad comercial ya saturada, sin novedad investigativa por sí sola— sino en resolver ese problema documentado con rigor de Ingeniería de Software. NAILA es una arquitectura de integración (Anti-Corruption Layer + Adapter) validada empíricamente sobre dos sistemas legacy reales y heterogéneos, que cuantifica, no solo afirma, el trade-off real entre mantenibilidad, esfuerzo de implementación y rendimiento al adoptarla frente a integrar sin arquitectura. Ninguna solución comercial de chat con IA publica ni sustenta con evidencia esa relación costo-beneficio de su propia arquitectura interna; esta investigación sí. Esa es la diferencia real: no es la interfaz conversacional, es la arquitectura validada detrás de ella y la evidencia empírica —estadísticamente confirmada, con limitaciones declaradas con honestidad— que la respalda.

## Resumen

NAILA propone y valida empíricamente una arquitectura (Anti-Corruption Layer + Adapter/API Facade) para incorporar agentes de IA generativa como capa de interacción en lenguaje natural sobre sistemas de software heredados, sin modificar su lógica de negocio. Se evalúa mediante dos casos de estudio (osCommerce v2.3.4 y Trac), comparando la arquitectura propuesta frente a una integración ad hoc mínima viable, en las dimensiones de mantenibilidad y eficiencia de desempeño (ISO/IEC 25010).

## Estado actual del proyecto

- ✅ Fase 0 — Preparación: ambos casos de estudio corriendo en Docker
- ✅ Fase 1 — Estado del arte: 15 fuentes documentadas, vacío de investigación consolidado, justificación formal
- ✅ Fase 2 — Diseño de arquitectura: diagrama de referencia, modelo LLM (Qwen3.5-9B), primer prototipo funcional
- ✅ Fase 3 — Implementación completa: ambos casos de estudio (osCommerce, Trac), ambas versiones (NAILA y ad hoc), 3 casos de uso equivalentes por sistema, todos validados end-to-end
- ✅ Fase 4 — Instrumentación de métricas: rendimiento (latencia Nivel 1/2), mantenibilidad (CBO, complejidad ciclomática), esfuerzo de integración
- ✅ Fase 5 — Experimento comparativo formal: 120 mediciones (10 repeticiones × 3 casos × 4 escenarios), análisis estadístico, **trade-off central cuantificado**: NAILA mejora mantenibilidad a cambio de mayor esfuerzo y costo marginal de rendimiento en Nivel 1
- ✅ Fase 6 — Análisis de resultados y discusión: resultados, discusión conectada con literatura, limitaciones (amenazas a validez interna/externa/constructo/conclusión), conclusiones y trabajo futuro (10 líneas priorizadas)
- ✅ Fase 7 — Demo funcional: chat web conectado a NAILA sobre osCommerce, catálogo real clicable, interfaz pulida (prueba de concepto local, ver ADR-008)
- 🔄 Fase 8 — Redacción final del documento de tesis

## Resumen de implementación (Fase 3)

| Caso de estudio | NAILA | Ad hoc | Casos de uso | Incidentes técnicos |
|---|---|---|---|---|
| osCommerce v2.3.4 | ✅ | ✅ | Listar productos, buscar por nombre, estado de pedido | 2 (esquema `orders_total`, pérdida de datos por volumen no persistente) |
| Trac | ✅ | ✅ | Listar tickets, buscar por palabra clave, detalles de ticket | 0 |


## Estructura del repositorio

```
naila-thesis/
├── investigacion/
│   ├── bitacora.md              → registro diario de avance
│   └── estado-del-arte.md       → 15 fuentes académicas documentadas
├── documentos-tesis/
│   ├── justificacion.md
│   ├── decisiones-arquitectonicas.md   → ADRs (7 decisiones documentadas)
│   ├── incidentes-tecnicos.md          → 6 incidentes con causa/solución
│   └── operacionalizacion-variables.md → definición de métricas
├── arquitectura/
│   └── arquitectura-naila.md    → diagrama + contratos de datos
├── casos-estudio/
│   ├── oscommerce/
│   │   ├── catalog/             → código fuente de osCommerce v2.3.4 (sin modificar)
│   │   ├── integracion-naila/   → Adapter + ACL (arquitectura propuesta) ✅
│   │   └── integracion-adhoc/   → baseline sin patrón ✅
│   └── trac/
│       ├── data/                → entorno Trac
│       ├── integracion-naila/   → Adapter + ACL ✅
│       └── integracion-adhoc/   → baseline sin patrón ✅
├── demo/                        → demo funcional empaquetado (docker-compose up --build)
│   ├── backend/                 → FastAPI + Dockerfile
│   ├── frontend/                → HTML/CSS/JS + Dockerfile (nginx)
│   ├── docker-compose.yml
│   └── README.md
└── metricas/                    → scripts y resultados de medición (Fase 4)
```

## Requisitos técnicos

- Docker Desktop
- Python 3.11+ (para la capa de integración)
- Ollama con el modelo `qwen3.5:9b`

## Patrón arquitectónico

Anti-Corruption Layer (Evans, 2003) + Adapter/API Facade (Gamma et al., 1994), aplicados a la integración de agentes de IA generativa — ver `documentos-tesis/decisiones-arquitectonicas.md` (ADR-002 a ADR-006) y `investigacion/estado-del-arte.md` para la fundamentación completa.
