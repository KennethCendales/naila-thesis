# NAILA — Non-Invasive Architecture for Integrating LLM Agents

**Tesis:** Arquitectura no invasiva para la integración de agentes de IA generativa en sistemas de software heredados: evaluación empírica de rendimiento y mantenibilidad mediante casos de estudio múltiples

**Autor:** Kenneth Cendales — Universidad Manuela Beltrán

## Resumen

NAILA propone y valida empíricamente una arquitectura (Anti-Corruption Layer + Adapter/API Facade) para incorporar agentes de IA generativa como capa de interacción en lenguaje natural sobre sistemas de software heredados, sin modificar su lógica de negocio. Se evalúa mediante dos casos de estudio (osCommerce v2.3.4 y Trac), comparando la arquitectura propuesta frente a una integración ad hoc mínima viable, en las dimensiones de mantenibilidad y eficiencia de desempeño (ISO/IEC 25010).

## Estado actual del proyecto

- ✅ Fase 0 — Preparación: ambos casos de estudio corriendo en Docker
- ✅ Fase 1 — Estado del arte: 15 fuentes documentadas, vacío de investigación consolidado, justificación formal
- ✅ Fase 2 — Diseño de arquitectura: diagrama de referencia, modelo LLM (Qwen3.5-9B), primer prototipo funcional
- ✅ Fase 3 — Implementación completa: ambos casos de estudio (osCommerce, Trac), ambas versiones (NAILA y ad hoc), 3 casos de uso equivalentes por sistema, todos validados end-to-end
- 🔄 Fase 4 — Instrumentación de métricas (CBO, complejidad ciclomática, latencia, throughput)
- ⏳ Fase 5 — Ejecución del experimento comparativo
- ⏳ Fase 6 — Análisis de resultados
- ⏳ Fase 7 — Redacción de tesis

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
└── metricas/                    → scripts y resultados de medición (Fase 4)
```

## Requisitos técnicos

- Docker Desktop
- Python 3.11+ (para la capa de integración)
- Ollama con el modelo `qwen3.5:9b`

## Patrón arquitectónico

Anti-Corruption Layer (Evans, 2003) + Adapter/API Facade (Gamma et al., 1994), aplicados a la integración de agentes de IA generativa — ver `documentos-tesis/decisiones-arquitectonicas.md` (ADR-002 a ADR-006) y `investigacion/estado-del-arte.md` para la fundamentación completa.
