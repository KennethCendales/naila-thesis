# Guía de Aplicación de NAILA a Nuevos Sistemas Legacy

> Este documento responde al objetivo específico 5 de la tesis: derivar lineamientos generalizables sobre la viabilidad del enfoque NAILA en contextos empresariales reales, más allá de los dos casos de estudio evaluados empíricamente.

## Contrato genérico (`naila_core.py`)

NAILA define dos abstracciones reutilizables, independientes del sistema legacy de destino:

- **`BaseACL`**: contrato mínimo que exige implementar `_connect()` (conexión al mecanismo de persistencia del legacy) y ofrece `to_canonical()`, un helper reutilizable para traducir registros crudos hacia el modelo canónico de NAILA mediante un mapeo declarativo de campos.
- **`BaseAdapter`**: contrato mínimo que exige recibir una instancia de `BaseACL` y declarar `tool_definitions`, la lista de operaciones expuestas al agente de IA.

Se demostró (ver `arquitectura/naila-core/ejemplos/`) que tanto `OsCommerceACL` (MySQL) como `TracACL` (SQLite) pueden implementar formalmente este contrato compartido, a pesar de operar sobre mecanismos de persistencia y dominios de datos completamente distintos (e-commerce vs. gestión de proyectos) — evidencia de que la abstracción no fue diseñada ad-hoc para un solo caso.

## Pasos para aplicar NAILA a un sistema legacy nuevo

### 1. Identificar el punto de integración de solo lectura
Determinar cómo acceder a los datos del sistema legacy sin modificar su lógica de negocio: acceso directo a base de datos (como en ambos casos de estudio), lectura de archivos, o una API existente si el sistema la expone. Se recomienda, siguiendo la práctica identificada en la literatura (ver `estado-del-arte.md`, fuente #8), comenzar siempre con operaciones de solo lectura antes de considerar escritura.

### 2. Definir el modelo canónico
Especificar qué campos y estructuras de datos expondrá la integración hacia el agente de IA, independientemente de cómo estén almacenados internamente en el legacy. Este modelo debe ser estable aunque el esquema interno del legacy cambie.

### 3. Implementar una clase que extienda `BaseACL`
- Implementar `_connect()` con el mecanismo de conexión específico del sistema (driver de base de datos, apertura de archivo, cliente HTTP, etc.).
- Para cada operación, definir un `field_mapping` (diccionario canónico → campo legacy) y usar `to_canonical()` para la traducción, evitando reescribir manualmente la construcción de diccionarios en cada método.

### 4. Implementar una clase que extienda `BaseAdapter`
- Recibir la instancia de la ACL en el constructor.
- Exponer métodos simples (uno por caso de uso) que deleguen en la ACL.
- Declarar `tool_definitions` en el formato de tool-calling del proveedor de LLM elegido (el proyecto usó el formato nativo de Ollama; otros proveedores como OpenAI o Anthropic usan formatos similares pero no idénticos — verificar la documentación específica).

### 5. Validar con pruebas end-to-end antes de escalar
Siguiendo la metodología aplicada en los Días 14-20 del proyecto: validar un caso de uso simple de punta a punta antes de agregar más operaciones, y crear una versión ad hoc de comparación solo si se desea replicar el estudio empírico de mantenibilidad/rendimiento.

### 6. (Opcional) Replicar la medición empírica
Si se desea cuantificar el trade-off de mantenibilidad/rendimiento para el nuevo sistema (como se hizo en las Fases 4-5 de esta tesis), se recomienda:
- Mantener separados los archivos de producción de los de prueba (ver definición operacional del Día 12/21)
- Fijar explícitamente los parámetros en las pruebas para controlar la variabilidad del LLM (lección del Día 17/23/26)
- Ejecutar múltiples repeticiones (se usaron 10 en este proyecto) para obtener significancia estadística

## Limitaciones de esta generalización

- El contrato genérico fue validado sobre dos sistemas con acceso de **solo lectura vía base de datos** (MySQL, SQLite). No se ha probado su aplicabilidad a sistemas que requieran escritura, ni a sistemas cuyo único punto de integración sea una API HTTP o un protocolo distinto (ej. SOAP, mensajería asíncrona) — esto queda como línea de trabajo futuro explícita.
- `to_canonical()` asume que los datos crudos del legacy llegan como estructuras tipo diccionario (filas de base de datos) — sistemas con formatos de datos más complejos (XML anidado, binarios propietarios) requerirían extender el contrato base con lógica de traducción adicional no cubierta por esta primera versión.
- Esta guía y los ejemplos ilustrativos no fueron sometidos a la misma validación empírica formal (Fases 4-5) que las implementaciones originales — se presentan como evidencia conceptual de generalizabilidad, no como un tercer caso de estudio medido con el mismo rigor.
