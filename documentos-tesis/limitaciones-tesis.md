# Limitaciones — NAILA

> Nota metodológica: esta sección se organiza siguiendo las categorías estándar de amenazas a la validez usadas en estudios empíricos de Ingeniería de Software (validez interna, externa, de constructo y de conclusión). Si tu universidad exige una cita formal para este marco (ej. Wohlin et al., *Experimentation in Software Engineering*), verifícala e inclúyela — no se cita aquí una fuente específica porque no fue verificada dentro de la revisión de literatura de este proyecto (`estado-del-arte.md`).

## 1. Amenazas a la validez interna

**Un solo investigador implementó ambas versiones (NAILA y ad hoc) en ambos casos de estudio.** Esto introduce dos riesgos relacionados pero distintos:
- *Efecto de aprendizaje*: la familiaridad adquirida al implementar la primera versión de un caso de estudio pudo reducir artificialmente el tiempo reportado para la segunda versión del mismo sistema, independientemente de la arquitectura empleada.
- *Riesgo de sesgo de confirmación*: al ser el mismo investigador quien diseñó la hipótesis (NAILA es más mantenible) y quien construyó deliberadamente la versión ad hoc como contraste, existe un riesgo no eliminado de que esta última se haya implementado de forma menos cuidadosa de lo que un desarrollador externo, sin conocimiento de la hipótesis, habría hecho. Se mitigó parcialmente exigiendo que ambas versiones resolvieran exactamente los mismos casos de uso con resultados idénticos (validado en los Días 17 y 20), pero no se eliminó por completo mediante, por ejemplo, una implementación a cargo de un tercero.

**El esfuerzo de integración fue auto-reportado en bloques aproximados**, no cronometrado con precisión de minutos (declarado en el Día 25), lo que introduce imprecisión en una de las tres dimensiones centrales de comparación.

## 2. Amenazas a la validez de constructo

**Las métricas de mantenibilidad son proxies, no mediciones directas de mantenibilidad percibida.** CBO y complejidad ciclomática son indicadores ampliamente usados en la literatura, pero ningún desarrollador externo al proyecto intentó modificar o extender el código para validar si estas métricas se correlacionan, en este caso específico, con dificultad real de mantenimiento percibida por terceros.

**El script propio de cálculo de CBO tiene una limitación conocida y documentada** (Día 22/24): no distingue entre acoplamiento a clases y acoplamiento a funciones del mismo módulo importado, por lo que los valores absolutos deben interpretarse con cautela; se argumentó que la comparación *relativa* entre NAILA y ad hoc permanece válida al aplicarse el mismo criterio de forma consistente, pero esto no elimina la imprecisión del constructo en términos absolutos.

**"Esfuerzo de integración" no tiene una operacionalización estandarizada única en la literatura** (declarado en `operacionalizacion-variables.md`), por lo que la definición usada en este estudio (horas + componentes afectados + SLOC) es una construcción propia, razonable pero no universalmente validada.

## 3. Amenazas a la validez externa (generalización)

**El estudio se basa en dos casos de estudio**, lo cual limita severamente la generalización estadística a la diversidad de sistemas legacy existentes en la práctica empresarial real. Ambos son proyectos de código abierto de tamaño moderado; ninguno representa la escala, antigüedad extrema, o heterogeneidad tecnológica (múltiples lenguajes, dependencias circulares complejas) de muchos sistemas legacy empresariales reales.

**Ambos casos de estudio se integraron mediante acceso de solo lectura.** No se validó el patrón arquitectónico para operaciones de escritura sobre el sistema legacy, un escenario con requisitos adicionales de seguridad, transaccionalidad y manejo de errores no explorados en este trabajo.

**Los resultados de rendimiento son específicos del hardware y modelo de LLM usados** (PC de sobremesa con Ryzen 7 5700G / RTX 3060, Qwen3.5-9B local vía Ollama — ver `operacionalizacion-variables.md`). No se comparó el comportamiento con modelos comerciales (Claude, GPT) ni con hardware de distinta capacidad, por lo que las cifras absolutas de latencia no deben generalizarse fuera de este contexto específico — sí se argumenta, en cambio, que la metodología de medición (separación en dos niveles) es generalizable independientemente del hardware o modelo usado.

**La validación de generalización del núcleo abstracto (`naila_core.py`)** se realizó de forma ilustrativa (ver guía de generalización), no con el mismo rigor empírico que los dos casos de estudio principales — no constituye un tercer caso de estudio medido, sino evidencia de diseño complementaria.

## 4. Amenazas a la validez de conclusión (estadística)

**El experimento comparativo formal (Día 26) usó n=30 mediciones por escenario** (10 repeticiones × 3 casos de uso), lo cual es razonable para observar tendencias con desviación estándar, pero no se aplicaron pruebas de significancia estadística formales (ej. prueba t, Mann-Whitney) para confirmar que las diferencias observadas entre NAILA y ad hoc no se deben al azar. Las conclusiones sobre el trade-off se basan en la comparación de medias y desviaciones estándar, un análisis descriptivo robusto pero no equivalente a una prueba de hipótesis formal.

**Se identificó y trató un valor atípico de arranque en frío** (Trac NAILA, Día 26) de forma transparente, pero su presencia indica que las mediciones de latencia son sensibles a condiciones de ejecución (estado de caché del sistema operativo, por ejemplo) no completamente controladas entre repeticiones.

## Síntesis

Estas limitaciones no invalidan los hallazgos centrales de la investigación, pero delimitan con precisión su alcance: **los resultados son evidencia empírica sólida sobre dos casos de estudio específicos, con una metodología de medición generalizable, pero no constituyen una generalización estadística validada a la diversidad de sistemas legacy empresariales reales.** Esta delimitación honesta es, en sí misma, parte del rigor metodológico que sustenta la credibilidad del trabajo.
