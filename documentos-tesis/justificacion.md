# Justificación — NAILA

## 1. Justificación desde la brecha científica

La integración de inteligencia artificial generativa en sistemas de software ha experimentado un crecimiento acelerado en la producción académica reciente: solo entre 2024 y 2025 se concentra la gran mayoría de la literatura sobre agentes basados en modelos de lenguaje aplicados a Ingeniería de Software (ver `estado-del-arte.md`, fuentes #3, #6). Sin embargo, este crecimiento no se ha traducido en consenso arquitectónico. Bucaioni et al. (2025) señalan explícitamente que la ausencia de una arquitectura de referencia comúnmente aceptada dificulta el razonamiento sistemático sobre el diseño, la evaluación y la evolución de sistemas integrados con LLM — y su propia propuesta, siendo la más cercana identificada en esta revisión, permanece en estado conceptual, sin validación empírica.

Paralelamente, la investigación que sí combina modelos de lenguaje con sistemas heredados resuelve problemas adyacentes pero distintos al que aquí se plantea: la recuperación asistida por IA de arquitectura legacy (ArchAgent) atiende la *comprensión* de sistemas existentes, no su *extensión funcional*; y los sistemas multiagente basados en LLM para Ingeniería de Software se orientan a la colaboración entre agentes durante el *desarrollo* de software, no a la interacción de un agente con un sistema ya desplegado en producción.

Esta investigación se justifica, en primer lugar, porque **ningún trabajo identificado combina los tres elementos centrales de NAILA de forma simultánea y validada empíricamente**: (1) un patrón arquitectónico no invasivo, (2) aplicado específicamente a agentes de IA generativa basados en LLM, (3) sobre sistemas de software heredados en el sentido estricto de la Ingeniería de Software (sistemas en producción, sin arquitectura moderna, sin API nativa, con deuda técnica documentada).

## 2. Justificación desde el rigor metodológico

Los patrones arquitectónicos que sustentan la propuesta —Anti-Corruption Layer (Evans, 2003) y Adapter (Gamma et al., 1994)— cuentan con más de dos décadas de uso consolidado en la práctica de la industria, y al menos un estudio empírico (ver `estado-del-arte.md`, fuente #11) que valida su impacto positivo sobre la mantenibilidad del software mediante un diseño comparativo (versión con patrón vs. versión sin patrón) — precedente metodológico directo del diseño experimental adoptado en esta tesis. No obstante, ese precedente no ha sido evaluado en el contexto específico de agentes de IA generativa, lo que representa una oportunidad concreta de extender un enfoque metodológico validado hacia un dominio de aplicación no explorado.

## 3. Justificación desde el impacto práctico

Los sistemas de software heredados representan una realidad extendida y persistente en las organizaciones: continúan operando en producción, sostienen procesos de negocio críticos, y su reemplazo completo suele ser económica y operativamente inviable en el corto o mediano plazo. La incorporación de capacidades de IA generativa sobre estos sistemas es, en consecuencia, un problema de relevancia práctica inmediata para organizaciones que no pueden —ni necesariamente deben— reescribir su infraestructura existente para beneficiarse de estas capacidades.

Es importante delimitar con precisión el alcance del aporte de esta investigación: **no se busca mejorar los sistemas seleccionados como casos de estudio (osCommerce, Trac) en sí mismos**, sino **proponer y validar empíricamente una arquitectura de integración generalizable**, de la cual osCommerce y Trac son únicamente los instrumentos de validación empírica, no el objeto final de mejora. Esta distinción es central para comprender la naturaleza de la contribución científica de la tesis: el aporte reside en el conocimiento arquitectónico generado y validado, no en el estado final de los sistemas utilizados como casos de estudio.

## 4. Síntesis

En conjunto, estas tres dimensiones —la brecha científica identificada, el rigor metodológico heredado de patrones y precedentes empíricos consolidados, y la relevancia práctica del problema de integración de IA sobre sistemas heredados— constituyen la justificación integral del proyecto NAILA como una contribución original, metodológicamente fundamentada y de aplicabilidad práctica a la Ingeniería de Software contemporánea.
