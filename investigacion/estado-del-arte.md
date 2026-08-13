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

---

# Día 7 — Fundamentación académica: patrones arquitectónicos (ACL, Adapter)

## 9. Evans, E. (2003) — *Domain-Driven Design: Tackling Complexity in the Heart of Software*

**Aporte principal:** <cite index="37-1">Fuente original del patrón Anti-Corruption Layer — describe la situación en la que dos sistemas necesitan comunicarse y, si son incompatibles, requieren una capa delegada de comunicación para asegurar que las solicitudes y respuestas sean entendidas por ambos sistemas. El ACL se compone de tres elementos: una fachada, un adaptador y un traductor</cite>.

**Limitaciones:** Es un libro de práctica de la industria (no un paper revisado por pares), aunque es la fuente primaria universalmente reconocida y citada en toda la literatura posterior sobre el patrón — su autoridad viene de haber acuñado y formalizado el concepto, no de metodología empírica.

**Relación con NAILA:** **Esta es la cita académica correcta para fundamentar el "ACL" de tu arquitectura** — reemplaza cualquier referencia genérica a "documentación de Microsoft" que usamos como atajo el Día 6. Cita completa: Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley Professional.

---

## 10. Gamma, Helm, Johnson & Vlissides (1994) — *Design Patterns: Elements of Reusable Object-Oriented Software*

**Aporte principal:** Fuente primaria del patrón Adapter (y los otros 22 patrones "Gang of Four"), clasificado como patrón estructural — <cite index="48-1">los patrones estructurales se ocupan de la composición de objetos, especificando cómo combinar elementos para lograr funcionalidad adicional (ej. adapter, composite, proxy, flyweight, facade, bridge, decorator)</cite>.

**Limitaciones:** Igual que Evans (2003), es un libro fundacional de práctica, no un estudio empírico — pero es la cita obligatoria y universalmente reconocida para el patrón Adapter.

**Relación con NAILA:** Cita completa: Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.

---

## 11. ⭐ "Empirical Investigation of the Impact of the Adapter Design Pattern on Software Maintainability" (IEEE)

**Aporte principal — el hallazgo más importante del día:** Este es un estudio empírico que usa **exactamente tu mismo diseño metodológico**: <cite index="62-1">se aplicaron técnicas de refactorización para generar una versión sin el patrón para cuatro sistemas sujetos de estudio, luego se calcularon y compararon métricas de software para ambas versiones (la versión con el patrón y la versión sin el patrón)</cite>. <cite index="62-1">Los resultados empíricos muestran que las versiones con el patrón Adapter tienen mejores métricas de software que las versiones sin el patrón, lo cual es una señal de que el patrón Adapter impacta positivamente la mantenibilidad del software</cite>.

**Limitaciones:** Solo 4 sistemas de estudio (tamaño de muestra similar al tuyo, lo cual es tanto una limitación compartida como un precedente que legitima tu propio tamaño de muestra); no se especifica si los sistemas eran legacy reales o proyectos de otro tipo — hay que revisar el paper completo para confirmarlo.

**Relación con NAILA — esta es la fuente más importante encontrada hasta ahora:** Este paper es **precedente metodológico directo** de tu diseño experimental (comparar versión con patrón vs. sin patrón, usando métricas de software). Te permite argumentar que tu metodología no es inventada, sino que sigue un enfoque ya validado en la literatura — solo que tú lo aplicas específicamente al contexto de integración de agentes LLM sobre sistemas heredados, que es donde está tu aporte original. **Prioridad para el Día 8: conseguir el texto completo de este paper (IEEE Xplore) y revisar qué métricas exactas usaron**, para comparar con tu tabla de CBO/complejidad ciclomática.

---

## 12. Otras referencias de aplicación de Adapter en integración legacy (contexto industrial)

Varias fuentes de práctica (KapreSoft, AlgoMaster, Belatrix) confirman de forma consistente el uso del patrón Adapter específicamente para integración con sistemas heredados — <cite index="60-1">el patrón Adapter resuelve esto introduciendo una clase envolvente que se sitúa entre tu sistema y el componente incompatible, traduciendo llamadas de tu interfaz hacia llamadas que el sistema legacy o de terceros entiende, sin cambiar ninguno de los dos lados</cite>. Esto es coherente con lo encontrado en osCommerce/Trac: ninguno expone una API moderna, por lo que el Adapter es la pieza que traduce las llamadas del agente hacia las funciones internas de cada sistema.

**Relación con NAILA:** Confirma consenso de la industria sobre la aplicabilidad del patrón a tu escenario exacto — útil como respaldo adicional, aunque de menor peso académico que las fuentes 9, 10 y 11.

---

## Síntesis actualizada — justificación del patrón arquitectónico

Con las fuentes del Día 6 y Día 7 combinadas, la justificación de "ACL + Adapter" para NAILA queda fundamentada en tres niveles:

1. **Fuente primaria/fundacional:** Evans (2003) para ACL, Gamma et al. (1994) para Adapter — establecen el patrón formalmente.
2. **Evidencia empírica de impacto en mantenibilidad:** El paper IEEE (#11) valida empíricamente que el patrón Adapter mejora métricas de software — precedente metodológico directo para tu propio experimento.
3. **Vacío específico que NAILA cubre:** Ninguna de estas fuentes aplica estos patrones específicamente a la integración de **agentes de IA generativa** sobre sistemas heredados — el patrón está fundamentado, pero su aplicación a este dominio específico (agentes LLM) es donde está tu contribución original, reforzado por lo encontrado el Día 6 (Bucaioni et al. confirmando la ausencia de arquitectura de referencia para sistemas LLM-integrados).

---

# Día 8 — Fundamentación de métricas de rendimiento (latencia, throughput)

## 13. "Evaluating Prompt Injection Defenses for Educational LLM Tutors: Security-Usability-Latency Trade-offs" (2026)

**Aporte principal — hallazgo metodológico clave del día:** Este paper mide el overhead de una arquitectura por capas (similar en espíritu a tu ACL + Adapter) sobre un sistema que usa LLM, y aplica una técnica de aislamiento importante: <cite index="73-1">el promedio de extremo a extremo para el adaptador completo de múltiples capas es de 2.50 ms, preservando el comportamiento interactivo mientras mejora la robustez frente al filtrado solo por expresiones regulares. Es fundamental notar que las métricas de latencia absolutas dependen fuertemente de la infraestructura de hardware subyacente, por lo que la cifra debe interpretarse como el overhead local añadido por el framework en relación con un baseline sin defensa, no como una garantía universal</cite>.

**Limitaciones:** El dominio de aplicación (tutores educativos con defensas contra prompt injection) es distinto al tuyo, pero la técnica de medición es directamente aplicable.

**Relación con NAILA — importante decisión metodológica que debes adoptar:** Este paper confirma la práctica correcta que ya habíamos definido intuitivamente en tu Nivel 1 de medición: **medir el overhead de la capa de integración de forma aislada, relativa a un baseline, no como cifra absoluta**. Además, remarca algo que debes incluir en tu apartado de limitaciones metodológicas: los resultados de latencia dependen del hardware usado y no deben presentarse como universales — debes ser explícito en tu tesis sobre las especificaciones de tu máquina de pruebas (tu laptop HP OMEN 16) para que los resultados sean reproducibles/interpretables correctamente.

---

## 14. "A Layered Security Framework Against Prompt Injection in RAG-Based Chatbots" (2026)

**Aporte principal:** Otro ejemplo reciente de medición de overhead por capas en un sistema que usa LLM — <cite index="77-1">la latencia de extremo a extremo se mide desde la recepción del input del usuario hasta la entrega de la respuesta, promediada sobre 500 consultas benignas por modelo en el hardware de despliegue local. La inferencia del LLM se excluye de la medición de overhead por capa, para aislar el costo atribuible específicamente al framework</cite>.

**Limitaciones:** Nuevamente, dominio distinto (seguridad de chatbots RAG), pero la metodología de medición es un precedente directo.

**Relación con NAILA — refuerza la decisión anterior:** Este es el segundo paper que confirma la misma práctica: **excluir el tiempo de inferencia del LLM en sí (que no controlas ni es tu variable de interés) del overhead medido de tu capa de integración**. Esto es exactamente coherente con tu diseño de "Nivel 1: capa de integración" — debes medir el tiempo que añade tu ACL/Adapter, no el tiempo que tarda el modelo de lenguaje en pensar, ya que eso último no es parte de tu contribución arquitectónica.

**Ajuste recomendado a tu tabla de métricas:** Cuando definas exactamente cómo medir "latencia" en el Nivel 1, especifica que se debe **excluir el tiempo de inferencia del LLM**, midiendo solo el tiempo entre "el adaptador recibe la intención estructurada" y "el adaptador entrega el resultado traducido desde el sistema legacy" — esto aísla tu verdadera contribución arquitectónica del tiempo de respuesta del modelo, que no controlas.

---

## 15. "GPU-Virt-Bench" / patrón general de medición de overhead de virtualización (2026)

**Aporte principal:** Aunque de un dominio técnico distinto (virtualización de GPU), aporta un patrón metodológico reutilizable: <cite index="71-1">medir el mismo tipo de llamada tanto bajo ejecución nativa como bajo la capa que se está evaluando, y calcular la diferencia para aislar el overhead de la capa (overhead = tiempo_con_capa - tiempo_nativo)</cite>.

**Limitaciones:** No es del dominio de sistemas legacy ni de IA — se cita únicamente por su valor metodológico de "medición diferencial", ampliamente generalizable.

**Relación con NAILA:** Confirma el diseño de tu Nivel 2 (sistema completo antes/después) — la fórmula "overhead = con_capa − sin_capa" es exactamente la comparación entre tu arquitectura NAILA y el baseline ad hoc que ya definiste.

---

## Síntesis del Día 8 — ajuste metodológico importante

El hallazgo más importante de hoy no es solo bibliográfico, es un **ajuste a tu diseño experimental**: al menos dos papers recientes (2026) que miden arquitecturas por capas sobre sistemas con LLM coinciden en la misma práctica — **excluir el tiempo de inferencia del LLM del overhead medido de la capa de integración**, y **declarar explícitamente las limitaciones de hardware** al reportar cifras de latencia. Vale la pena que ajustes la definición operacional de "latencia" en tu tabla de métricas (Día del sql_mode... perdón, de la tabla de operacionalización) para incorporar esta exclusión — mejora sustancialmente el rigor metodológico de tu Nivel 1.

---

# Día 9 — Vacíos de investigación (Research Gap)

> Síntesis formal de por qué NAILA es necesaria, basada en las 15 fuentes recolectadas en los Días 6-8. Esta sección está redactada para poder trasladarse casi directamente a la tesis (con ajustes menores de estilo académico).

## Vacío 1 — Ausencia de arquitectura de referencia validada empíricamente para sistemas LLM-integrados

La literatura reciente reconoce explícitamente este vacío: Bucaioni et al. (2025) señalan que la ausencia de una arquitectura de referencia comúnmente aceptada dificulta el razonamiento sistemático sobre el diseño de sistemas integrados con LLM (ver fuente #1). Sin embargo, su propuesta es puramente conceptual, sin validación empírica. **NAILA cubre esta brecha aplicando y validando empíricamente un patrón arquitectónico específico (ACL + Adapter), en vez de proponer un marco teórico general sin probar.**

## Vacío 2 — La investigación sobre LLM + sistemas heredados existe, pero resuelve un problema distinto

Los trabajos más recientes que combinan LLM y sistemas legacy (ej. ArchAgent, fuente #2) se enfocan en **comprensión/recuperación de arquitectura** (ingeniería inversa asistida por IA), no en **integración funcional de nuevas capacidades** sobre el sistema en producción. De forma similar, la literatura de sistemas multiagente LLM para Ingeniería de Software (fuente #3) se concentra en agentes que colaboran entre sí durante el *desarrollo* de software, no en agentes que sirven como capa de interacción de usuario final sobre un sistema ya desplegado. **NAILA aborda específicamente el escenario no cubierto: un agente LLM como interfaz de interacción sobre un sistema heredado en producción, sin modificar su lógica de negocio.**

## Vacío 3 — Los patrones arquitectónicos (ACL, Adapter) están fundamentados, pero no aplicados ni validados en el contexto específico de agentes de IA generativa

ACL (Evans, 2003) y Adapter (Gamma et al., 1994) son patrones consolidados de más de dos décadas, con al menos un estudio empírico que valida el impacto positivo del Adapter sobre mantenibilidad (fuente #11). Sin embargo, ese estudio (como el resto de la literatura de patrones de diseño) no evalúa su aplicación al escenario específico de integrar un **agente de IA generativa basado en LLM** sobre un sistema heredado. **NAILA extiende la validación empírica de estos patrones consolidados a un dominio de aplicación nuevo y no explorado.**

## Vacío 4 — Predominancia de contenido de práctica industrial sin rigor académico

Una parte significativa de lo disponible sobre "integración de IA en sistemas legacy" proviene de blogs de consultoras (Prismetric, fuente #8) o documentación de proveedores (Microsoft Azure), no de investigación revisada por pares. Esto no invalida su utilidad práctica, pero **evidencia que el conocimiento sobre este problema específico está fragmentado entre práctica no validada académicamente e investigación académica que resuelve problemas adyacentes pero no idénticos.** NAILA busca cerrar esa fragmentación con un estudio riguroso y reproducible.

## Vacío 5 — Ausencia de guías metodológicas específicas para medir el overhead de arquitecturas de integración con LLM

Aunque encontramos precedentes recientes (2026) de medición de overhead en arquitecturas por capas sobre sistemas con LLM (fuentes #13, #14), estos provienen de dominios de seguridad (defensas contra prompt injection), no de integración con sistemas heredados. **NAILA adapta y aplica esta metodología de medición (aislar el overhead de la capa, excluyendo la inferencia del LLM) a un dominio distinto, aportando una guía metodológica replicable para investigaciones futuras similares.**

---

## Declaración formal del vacío de investigación (versión consolidada para la tesis)

> A pesar del creciente interés académico e industrial por integrar inteligencia artificial generativa en sistemas de software, no existe, hasta la fecha de esta investigación, una arquitectura validada empíricamente que permita incorporar agentes basados en LLM como capa de interacción sobre sistemas de software heredados sin modificar su lógica de negocio central. Los trabajos existentes o bien proponen arquitecturas de referencia sin validación empírica (Bucaioni et al., 2025), o abordan problemas adyacentes como la recuperación de arquitectura legacy asistida por IA (ArchAgent) o la colaboración entre agentes durante el desarrollo de software, sin evaluar la integración de agentes como interfaz de usuario final sobre sistemas ya desplegados. Los patrones arquitectónicos que sustentan la propuesta de esta investigación (Anti-Corruption Layer, Adapter) cuentan con fundamentación teórica consolidada y al menos un precedente de validación empírica sobre mantenibilidad, pero no han sido evaluados en el contexto específico de agentes de IA generativa. Esta investigación busca cerrar dicho vacío mediante el diseño, implementación y evaluación empírica de una arquitectura no invasiva (NAILA), validada a través de casos de estudio múltiples sobre sistemas heredados reales de código abierto.

## Pendiente para el Día 10

Redactar la sección formal de "Justificación" del proyecto (punto 2 de la estructura de 19 puntos), integrando este vacío de investigación con el impacto práctico ya discutido en las primeras sesiones (la frase clave: "no se está mejorando osCommerce o Trac, se está proponiendo y validando una arquitectura de integración").



