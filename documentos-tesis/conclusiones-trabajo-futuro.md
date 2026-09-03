# Conclusiones y Trabajo Futuro — NAILA

## Conclusiones

### Cumplimiento de los objetivos específicos

**Objetivo 1 — Caracterizar los patrones arquitectónicos existentes para la integración de componentes de IA en sistemas heredados, e identificar el más adecuado para agentes basados en LLM.**
Cumplido. La revisión de literatura (Fase 1, 15 fuentes) permitió identificar que, si bien existen propuestas conceptuales recientes de arquitectura de referencia para sistemas LLM-integrados (Bucaioni et al., 2025), ninguna cuenta con validación empírica, y que los patrones Anti-Corruption Layer (Evans, 2003) y Adapter (Gamma et al., 1994) cuentan con fundamentación teórica sólida y al menos un precedente de validación empírica sobre mantenibilidad, aunque no aplicados previamente al dominio de agentes de IA generativa.

**Objetivo 2 — Diseñar una arquitectura de referencia que defina los mecanismos de comunicación, adaptación y seguridad mínima entre el agente de IA y el sistema heredado.**
Cumplido. Se diseñó la arquitectura NAILA (Día 11), formalizada posteriormente como contrato abstracto reutilizable (naila_core.py), con contratos de datos explícitos entre cada capa.

**Objetivo 3 — Implementar la arquitectura propuesta sobre 2 sistemas heredados de código abierto seleccionados como casos de estudio.**
Cumplido. Se implementaron ambas versiones (NAILA y ad hoc) sobre osCommerce v2.3.4 y Trac, con 3 casos de uso equivalentes por sistema, validados end-to-end (Fase 3).

**Objetivo 4 — Medir y comparar el impacto de la integración en métricas de mantenibilidad y rendimiento frente a una integración ad hoc mínima viable.**
Cumplido. Se ejecutaron 120 mediciones formales (Fase 4-5), encontrando que NAILA reduce la complejidad ciclomática promedio (22-32% según el caso) a cambio de mayor esfuerzo de implementación y un costo marginal de rendimiento en la capa de integración: un trade-off cuantificado, no solo enunciado.

**Objetivo 5 — Analizar los resultados obtenidos para derivar lineamientos generalizables sobre la viabilidad de este enfoque en contextos empresariales reales.**
Cumplido parcialmente. Se derivó una guía de generalización y se validó ilustrativamente que el contrato arquitectónico (naila_core.py) es aplicable a dos dominios heterogéneos. Sin embargo, como se detalla en la sección de Limitaciones (Día 29), esta generalización no cuenta con el mismo rigor empírico que los hallazgos de los objetivos 3 y 4: es evidencia de diseño, no un tercer caso de estudio medido con igual rigor.

### Respuesta a la pregunta de investigación

Esta investigación demuestra que es posible diseñar, implementar y validar empíricamente una arquitectura no invasiva para integrar agentes de IA generativa sobre sistemas de software heredados, y que dicha arquitectura presenta un trade-off cuantificable, no gratuito, entre mantenibilidad, esfuerzo de implementación y rendimiento. El vacío de investigación identificado (Día 9) se cierra parcialmente: se aporta la primera validación empírica conocida, dentro del alcance de la literatura revisada, de un patrón arquitectónico específico para este problema, aunque circunscrita a dos casos de estudio y sujeta a las limitaciones declaradas.

---

## Trabajo Futuro

Organizado por horizonte temporal, considerando que el investigador cuenta con aproximadamente un año adicional antes de la sustentación final, sobre una tesis ya completa y defendible en su forma actual.

### Corto plazo (semanas — mejoras de bajo costo, alto impacto sobre lo ya hecho)

1. Prueba de significancia estadística formal (t de Student u otra apropiada) sobre las 120 mediciones de latencia Nivel 1, para fortalecer la validez de conclusión ya declarada como limitación (Día 29).
2. Verificación de la causa raíz del outlier de arranque en frío en Trac NAILA (Día 26), si el tiempo lo permite, para descartar completamente su origen antes de la defensa.

### Mediano plazo (meses — extensiones sustanciales sobre la arquitectura actual)

3. Extensión a operaciones de escritura: diseñar y validar el mecanismo de la ACL/Adapter para operaciones que modifiquen el estado del sistema legacy (crear, actualizar, cancelar), con los requisitos adicionales que esto implica (transaccionalidad, autorización, auditoría de cambios): condición necesaria para casos de uso como agendar o modificar citas.
4. Aplicación a dominios regulados de alto valor social: universidades (agendamiento académico), hospitales (citas médicas), servicios públicos (trámites), cada uno con sus propios requisitos de cumplimiento normativo (ej. datos de salud) que deberán evaluarse específicamente antes de cualquier prueba con datos reales.
5. Comparación entre proveedores de LLM: replicar el experimento comparativo usando modelos comerciales (Gemini, GPT, Claude) además del modelo local (Qwen3.5-9B), para determinar si el trade-off encontrado es específico del modelo usado o se generaliza entre proveedores. Pospuesto deliberadamente por el costo asociado a las APIs comerciales en múltiples repeticiones.
6. Tercer y cuarto caso de estudio: ampliar la validación empírica a sistemas legacy adicionales, idealmente de mayor escala o de un dominio tecnológico distinto (ej. un sistema Java, o un sistema con API REST parcial existente), para fortalecer la validez externa más allá de los dos casos actuales.
7. Empaquetado y publicación de naila_core como librería instalable (PyPI), con documentación de uso independiente de la tesis.

### Largo plazo (dentro del año disponible — validación en condiciones reales)

8. Piloto con una organización real, siguiendo el proceso de aprobación ética correspondiente de la universidad, para validar NAILA en condiciones de producción genuinas: la extensión natural del demo funcional construido en la Fase 7, y la respuesta directa a la pregunta de si esto funciona fuera de un entorno controlado.
9. Estudio de mantenibilidad percibida con desarrolladores externos: reclutar desarrolladores sin conocimiento de la hipótesis de investigación para extender ambas versiones (NAILA y ad hoc) con una funcionalidad nueva, comparando su tiempo y dificultad percibida contra las métricas objetivas (CBO, complejidad ciclomática). Este estudio también mitigaría directamente la amenaza de validez interna relacionada con que un solo investigador implementó ambas versiones (Día 29).
10. Publicación académica derivada: preparar un artículo basado en los hallazgos de esta tesis para envío a una revista o conferencia de Ingeniería de Software, aprovechando el rigor metodológico ya alcanzado.

### Nota sobre el alcance de esta lista

Ninguno de estos diez puntos es un requisito para que la tesis actual sea válida y defendible: todos son extensiones legítimas para el trabajo futuro del investigador, no vacíos que invaliden lo ya logrado. Intentar resolverlos todos antes de la entrega actual repetiría el riesgo de alcance ya discutido explícitamente en el proyecto (ADR-008): una tesis que nunca cierra por perseguir una versión cada vez más completa.
