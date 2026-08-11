# Estado del Arte — NAILA
### Día 6 — Búsqueda sistemática: integración de IA/agentes en sistemas heredados

---

## 1. Bucaioni et al. (2025) — "A Functional Software Reference Architecture for LLM-Integrated Systems" (ICSA 2025)

**Aporte principal:** Propone una arquitectura de referencia funcional preliminar para sistemas integrados con LLM, <cite index="13-1">motivada por la ausencia de una arquitectura de referencia de software comúnmente aceptada, lo cual dificulta el razonamiento sistemático sobre su diseño y atributos de calidad</cite>. La arquitectura identifica capas como pre-procesamiento, inferencia central y post-procesamiento, <cite index="15-1">donde los componentes se comunican mediante APIs RESTful, gRPC para baja latencia, o mecanismos de caché compartidos</cite>.

**Limitaciones:** Es un trabajo de resultados "emergentes" (early-stage), sin validación empírica sobre sistemas reales — es puramente conceptual.

**Relación con NAILA:** Es el trabajo más cercano encontrado a la fecha — confirma que **no existe consenso arquitectónico establecido para sistemas LLM-integrados**, lo cual refuerza directamente el vacío de investigación de tu tesis. A diferencia de Bucaioni et al., NAILA no busca una arquitectura de referencia general, sino un patrón específico (ACL + Adapter) aplicado y validado empíricamente sobre sistemas heredados reales.

**Oportunidad de mejora que aprovecha NAILA:** Validación empírica mediante estudio de casos — exactamente lo que este trabajo no hace.

---

## 2. ArchAgent (2026) — "Scalable Legacy Software Architecture Recovery with LLMs"

**Aporte principal:** <cite index="5-1">Presenta un framework basado en agentes para recuperar arquitectura de software heredado a gran escala, combinando análisis estático y segmentación adaptativa de código</cite>, abordando el problema de que los LLM tienen contexto limitado frente a bases de código legacy extensas.

**Limitaciones:** Se enfoca en **recuperar/entender** arquitectura existente (ingeniería inversa), no en **integrar nuevas capacidades** de IA sobre el sistema legacy — es un objetivo distinto al de NAILA.

**Relación con NAILA:** Confirma que hay investigación activa reciente (2026) sobre LLMs + sistemas legacy, pero orientada a comprensión/documentación, no a integración funcional no invasiva. Refuerza el vacío específico que NAILA cubre.

---

## 3. Literature Review — "LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision and the Road Ahead" (ACM TOSEM, 2024-2025)

**Aporte principal:** Revisión sistemática sobre sistemas multiagente basados en LLM aplicados a Ingeniería de Software, <cite index="6-1">explorando el potencial transformador de integrar LLMs en agentes autónomos que ofrecen capacidades cognitivas competitivas con la planificación y razonamiento humano</cite>. <cite index="4-1">Especifica los datos intercambiados entre agentes, frecuentemente en forma de texto, incluyendo fragmentos de código, mensajes de commit, publicaciones de foros, reportes de errores o de vulnerabilidades</cite>.

**Limitaciones:** El foco está en agentes que colaboran entre sí para tareas de desarrollo de software (generación de código, testing), no en agentes que interactúan con sistemas de producción heredados como capa de usuario final.

**Relación con NAILA:** Útil como marco conceptual de qué es un "agente LLM" en el contexto de Ingeniería de Software, pero confirma que la literatura de agentes se concentra en asistir el *desarrollo*, no en la *integración con sistemas ya desplegados* — otro ángulo del vacío de NAILA.

---

## 4. "Artificial Intelligence for Software Architecture: Literature Review and the Road Ahead" (2025)

**Aporte principal:** Revisión amplia sobre el uso de IA en arquitectura de software, catalogando decenas de estudios recientes (2023-2025) sobre arquitecturas para sistemas con IA integrada, incluyendo pipelines de datos y sistemas de recomendación para conformidad arquitectónica.

**Limitaciones:** Es una revisión general del campo "IA para arquitectura de software" — no profundiza específicamente en el subproblema de integración no invasiva sobre sistemas heredados.

**Relación con NAILA:** Sirve como mapa del campo más amplio en el que se ubica tu tesis, y confirma la explosión reciente de publicaciones (2024-2025) en la intersección IA + arquitectura de software — consistente con lo que ya habíamos encontrado en la fase de definición del tema.

---

## 5. Microsoft Azure Architecture Center — "Anti-Corruption Layer Pattern"

**Aporte principal:** Documentación de referencia (no un paper académico, pero ampliamente citada en literatura técnica) sobre el patrón ACL. <cite index="20-1">El patrón puede aplicarse también a otras arquitecturas de servicio, como la integración de código heredado en una arquitectura monolítica</cite>, y recomienda <cite index="20-1">reforzar la validación y sanitización de entradas en esa frontera, además de planificar observabilidad, incluyendo IDs de correlación y logging estructurado, para diagnosticar fallos de traducción</cite>.

**Limitaciones:** Es documentación de práctica industrial, no investigación revisada por pares — debe citarse como fuente de patrón de diseño reconocido, no como evidencia empírica.

**Relación con NAILA:** Fundamenta directamente la elección del patrón ACL + Adapter que ya definiste para la arquitectura de NAILA, y aporta recomendaciones prácticas de implementación (observabilidad, logging) que puedes incorporar al diseño.

**Nota metodológica:** Para la tesis formal, conviene rastrear la fuente académica original del patrón ACL — proviene del libro de Eric Evans sobre Domain-Driven Design (2003), no de Microsoft. Microsoft documenta y populariza el patrón, pero la cita académica primaria debe ser Evans.

---

## 6. Chidamber & Kemerer (1994) y validaciones empíricas posteriores

**Aporte principal:** El paper original define la suite de métricas CK (incluyendo CBO). Estudios de validación posterior confirman su uso continuo: <cite index="31-1">un análisis de meta-análisis estadístico sobre 200 proyectos de dominio público encontró correlaciones entre moderadas y altas entre algunas de las métricas CK</cite>.

**Limitaciones:** La misma literatura de validación **advierte sobre limitaciones metodológicas** — <cite index="27-1">se han observado varias fallas e inconsistencias en el conjunto de seis métricas basadas en clases</cite>, y estudios de medición teórica señalan que <cite index="32-1">usando la medida de acoplamiento de objetos (CBO) como ejemplo, no establecer un sistema de relación empírica sólido puede llevar a deficiencias en las métricas de software</cite>.

**Relación con NAILA:** **Importante matiz para tu tesis** — no basta con citar CK como "la métrica estándar"; debes reconocer en tu marco teórico que CBO tiene limitaciones metodológicas documentadas, y justificar por qué sigue siendo apropiada para tu caso de uso (comparación relativa entre dos implementaciones, no medición absoluta de calidad).

---

## 7. "How effective are maintainability metrics in estimating maintenance efforts? An empirical study"

**Aporte principal:** <cite index="34-1">Con datos de industria de software desarrollado en dos lenguajes de programación populares en desarrollo orientado a objetos, las métricas están significativamente asociadas con defectos, aunque el efecto varía entre lenguajes (C++ y Java)</cite>.

**Limitaciones:** Estudio centrado en predicción de defectos/esfuerzo de mantenimiento general, no en el escenario específico de "antes/después de una integración puntual" que es tu diseño experimental.

**Relación con NAILA:** Refuerza que las métricas de mantenibilidad tienen relación empírica validada con esfuerzo real de mantenimiento — apoya la elección metodológica, aunque el contexto de aplicación es distinto (más amplio) al tuyo.

---

## 8. "AI Integration Architecture for Legacy Systems" (fuente de práctica industrial)

**Aporte principal:** Describe patrones de arquitectura usados en la industria para integrar IA sobre sistemas legacy (mainframes, ERPs, CRMs), incluyendo <cite index="23-1">una capa anti-corrupción que traduce esquemas legacy y conceptos de negocio hacia un modelo de datos canónico que los servicios más nuevos pueden entender</cite>, y recomienda <cite index="23-1">comenzar con acceso de solo lectura, para luego añadir acciones aprobadas una vez que los controles de seguridad y respaldo estén probados</cite>.

**Limitaciones:** Es contenido de consultora/blog técnico, sin revisión por pares ni validación empírica — usar con cautela, solo como evidencia de práctica de la industria, nunca como fuente académica primaria.

**Relación con NAILA:** Confirma el patrón "empieza con solo lectura, añade escritura después" como práctica común — un dato útil para el diseño incremental de tu prototipo (Fase 2), y evidencia adicional de que la literatura rigurosa sobre este tema específico es escasa frente al volumen de contenido de práctica/consultoría (tal como identificamos en la fase de definición del título).

---

## Síntesis del día — vacío de investigación reforzado

Con estas 8 fuentes, el argumento central se sostiene con más evidencia:

1. **Existe consenso sobre la necesidad** de arquitecturas específicas para integración de IA/LLM en software (Bucaioni et al. lo dice explícitamente).
2. **No existe un estándar arquitectónico validado empíricamente** — los trabajos encontrados son conceptuales (Bucaioni et al.) o de práctica industrial sin rigor académico (Prismetric, Azure Docs).
3. **La investigación sobre LLM + legacy existe pero apunta a otro problema** (recuperación/comprensión de arquitectura — ArchAgent) o a colaboración entre agentes para desarrollo (no integración con sistemas en producción).
4. **Las métricas que planeas usar (CBO, complejidad ciclomática) tienen validación empírica de décadas, pero con limitaciones metodológicas conocidas que debes reconocer explícitamente**, no ignorar.

## Pendiente para el Día 7

Profundizar específicamente en la fundamentación académica del patrón ACL (rastrear cita primaria de Evans, DDD) y buscar más literatura sobre el patrón Adapter en contextos de integración de sistemas.
