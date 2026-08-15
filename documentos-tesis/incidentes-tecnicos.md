# Registro de Incidentes Técnicos — NAILA

> A diferencia de las ADR (decisiones de diseño), aquí se documentan errores concretos encontrados durante la implementación, con su síntoma, causa y solución. Esto alimenta directamente una posible sección de "lecciones aprendidas" o anexo técnico de la tesis, y es evidencia de trabajo riguroso de troubleshooting.

---

## Incidente #001 — Conflicto de OneDrive con Git/Docker

**Fecha:** 3/8/2026
**Severidad:** Baja (preventivo, no bloqueante)
**Ver también:** ADR-001

**Síntoma:** Ninguno manifestado aún — identificado preventivamente antes de que causara fallos.

**Causa:** Carpeta del proyecto ubicada dentro del árbol sincronizado por OneDrive.

**Solución:** Mover carpeta completa a `C:\Users\kenneth\Documents\naila-thesis`.

**Tiempo perdido:** Mínimo (resuelto antes de generar problemas reales)

---

## Incidente #002 — Fallo de `apt-get update` por repositorios Debian inactivos

**Fecha:** 4/8/2026
**Severidad:** Media (bloqueante hasta resolver)
**Ver también:** ADR-003

**Síntoma:** Al construir el `Dockerfile` personalizado sobre `php:5.6-apache`, el comando `apt-get update` fallaba al no poder acceder a los repositorios Debian configurados por defecto.

**Causa raíz:** La versión de Debian base de la imagen `php:5.6-apache` alcanzó su fin de soporte (EOL); sus paquetes fueron movidos al archivo histórico `archive.debian.org`, y los repositorios activos (`deb.debian.org`, `security.debian.org`) ya no sirven esas versiones.

**Solución aplicada:**
```dockerfile
RUN sed -i \
    -e 's|deb.debian.org|archive.debian.org|g' \
    -e 's|security.debian.org|archive.debian.org|g' \
    /etc/apt/sources.list \
 && sed -i '/stretch-updates/d' /etc/apt/sources.list \
 && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid

RUN apt-get update --allow-insecure-repositories \
 && apt-get install -y --allow-unauthenticated [paquetes...]
```

**Tiempo perdido:** _(confirmar si lo recuerdas — aprox. 30-60 min)_

**Nota para la tesis:** Este incidente es en sí mismo un hallazgo interesante — documenta cómo *la infraestructura para reproducir un sistema legacy también se vuelve legacy con el tiempo*, lo cual podría mencionarse como una observación cualitativa en la discusión de resultados.

---

## Incidente #003 — Fallo de conexión PHP 5.6 → MySQL 5.7

**Fecha:** 4/8/2026
**Severidad:** Media (bloqueante hasta resolver)
**Ver también:** ADR-002

**Síntoma:** Error de conexión rechazada ("connection refused" / "can't connect to MySQL server") al intentar que el contenedor `web` (PHP 5.6 + extensión legacy `mysql`) se conectara al contenedor `db` corriendo `mysql:5.7`.

**Causa raíz:** No confirmada con certeza — hipótesis: incompatibilidad entre el driver legacy `ext/mysql` y cambios de protocolo/autenticación en MySQL 5.7. *(Pendiente: revisar logs exactos de `docker logs <contenedor-db>` en el momento del fallo para documentar causa con precisión antes de la redacción final de tesis.)*

**Solución aplicada:** Downgrade de la imagen de base de datos a `mysql:5.6`.

**Tiempo perdido:** _(confirmar si lo recuerdas)_

**Pendiente:** Verificar causa raíz exacta si el tiempo lo permite — mejora la calidad del hallazgo para la tesis.

---

## Incidente #004 — Fallo de importación de esquema por `sql_mode` estricto (`customers_dob`)

**Fecha:** 4/8/2026
**Severidad:** Media (bloqueante hasta resolver)
**Ver también:** ADR-002 (relacionado con la versión de MySQL usada)

**Síntoma:** Durante el paso de importación de base de datos del wizard de instalación de osCommerce, apareció el error: *"There was a problem importing the database. The following error had occurred: Invalid default value for 'customers_dob'"*.

**Causa raíz:** MySQL 5.6+ activa por defecto un `sql_mode` que incluye `NO_ZERO_DATE` y `STRICT_TRANS_TABLES`, el cual rechaza el valor `0000-00-00` como valor por defecto en columnas de tipo fecha. El esquema SQL original de osCommerce 2.3.4 (diseñado en 2014, para versiones de MySQL con `sql_mode` permisivo por defecto) usa ese valor en la columna `customers_dob`.

**Solución aplicada:** Se configuró el contenedor de MySQL para iniciar con un `sql_mode` relajado, agregando al `docker-compose.yml`:
```yaml
command: --sql-mode="NO_ENGINE_SUBSTITUTION"
```
Esto sustituye el `sql_mode` estricto por defecto por uno mínimo, compatible con el esquema legacy.

**Tiempo perdido:** Incluido dentro del tiempo total del Día 2 (no cuantificado por separado)

**Nota para la tesis:** Este es un segundo hallazgo (junto al Incidente #002) de fricción entre software legacy y comportamientos por defecto más estrictos en versiones modernas de su propia infraestructura de datos — refuerza el argumento de que "integrar sin modificar la lógica de negocio" no significa "sin fricción de compatibilidad de entorno", una distinción importante para la discusión de resultados.

---

## Incidente #005 — Columna `order_total` inexistente en tabla `orders` (esquema normalizado en tabla separada)

**Fecha:** Día 16, Fase 3
**Severidad:** Baja (bloqueante para el caso de uso específico, pero de solución directa)

**Síntoma:** Al ejecutar la consulta de estado de pedido, se obtuvo el error `pymysql.err.OperationalError: (1054, "Unknown column 'order_total' in 'field list'")`.

**Causa raíz:** osCommerce v2.3.4 no almacena el total del pedido como columna directa en la tabla `orders`. En su lugar, normaliza los conceptos del total (subtotal, envío, impuestos, total final) en una tabla separada, `orders_total`, con una fila por concepto, distinguida por la columna `class` (ej. `ot_total` para el total final).

**Solución aplicada:** Se modificó `OsCommerceACL.get_order_status()` para realizar una segunda consulta sobre `orders_total`, filtrando por `class = 'ot_total'`, y combinar el resultado con los datos de `orders`.

**Tiempo perdido:** Menor — diagnóstico directo a partir del mensaje de error de MySQL.

**Nota para la tesis:** Este incidente es un buen ejemplo cualitativo de **deuda de conocimiento del dominio legacy**: entender el esquema de datos de un sistema heredado no documentado formalmente requiere exploración empírica (inspeccionar tablas relacionadas), no solo lectura de documentación — un costo real de "esfuerzo de integración" que vale la pena mencionar en la discusión de resultados como parte de la experiencia cualitativa de trabajar con sistemas legacy, más allá de las métricas cuantitativas.

---

## Incidente #006 — Pérdida completa de base de datos por volumen Docker no persistente, y cadena de complicaciones en la recuperación

**Fecha:** Día 16 (cierre), Fase 3
**Severidad:** Alta (pérdida total de datos; cadena de 3 problemas secundarios durante la recuperación)

**Síntoma inicial:** Tras ejecutar `docker-compose up` nuevamente, la tienda dejó de cargar con el error `1146 - Table 'oscommerce.configuration' doesn't exist`.

**Causa raíz:** El `docker-compose.yml` de osCommerce nunca declaró un volumen con nombre para los datos de MySQL (`/var/lib/mysql`). Al recrearse el contenedor `db` (`docker-compose down` + `up`), Docker no tenía dónde persistir los datos previos, por lo que el nuevo contenedor inició con una base de datos completamente vacía. Todo el trabajo previo (tienda "Pola Store", productos, el pedido #1 usado para validar `get_order_status`) se perdió sin posibilidad de recuperación.

**Cadena de problemas secundarios durante la recuperación:**
1. Al intentar reinstalar, osCommerce no mostraba el wizard — porque `configure.php` seguía existiendo en disco (solo se perdieron los datos del contenedor de BD, no los archivos locales), y el sistema asumía que ya estaba instalado.
2. Al acceder directamente a `/install/index.php`, apareció un error adicional: la carpeta `/install` ya no existía (se había eliminado como parte del procedimiento normal de cierre del Día 2/16) — fue necesario recuperarla clonando temporalmente una copia limpia del repositorio oficial `osCommerce/oscommerce2` (tag `v2.3.4`) y copiando solo esa carpeta.
3. Al reintentar el wizard, apareció un error de permisos: el sistema no podía escribir en `configure.php` / `admin/configure.php` — fue necesario otorgar permisos temporales (`chmod 777`), y restringirlos de nuevo (`chmod 444`) tras completar la instalación, replicando la misma medida de seguridad aplicada en el Día 2.

**Solución aplicada (definitiva):** Se agregó un volumen con nombre en el `docker-compose.yml`:
```yaml
db:
  volumes:
    - db_data:/var/lib/mysql
volumes:
  db_data:
```
Con esto, los datos de MySQL persisten incluso si los contenedores se recrean, y solo se perderían con un `docker-compose down -v` explícito (bandera `-v`).

**Tiempo perdido:** Significativo — la recuperación completa (diagnóstico + 3 problemas en cascada + reinstalación completa + recreación de datos de prueba) tomó varias horas repartidas en la sesión.

**Nota para la tesis:** Este incidente es un hallazgo cualitativo valioso sobre el **costo real de mantener un entorno de desarrollo reproducible para un sistema legacy**: un descuido de configuración de infraestructura (volumen no persistente) generó una cascada de complicaciones no triviales para restaurar el estado del sistema. Es evidencia concreta de que "esfuerzo de integración" en la práctica incluye no solo escribir código de adaptación, sino también gestionar correctamente el ciclo de vida del entorno legacy — un costo operativo real que rara vez se captura en métricas puramente de código (CBO, complejidad ciclomática), y que vale la pena mencionar como limitación/observación cualitativa en la discusión de resultados.

---

## Plantilla para futuros incidentes

```markdown
## Incidente #00N — [Descripción corta]

**Fecha:**
**Severidad:** Baja / Media / Alta (¿bloqueó el avance por completo?)

**Síntoma:** (¿Qué error/comportamiento viste exactamente? Copia el mensaje literal si lo tienes)

**Causa raíz:** (¿Por qué pasó? Si no estás 100% seguro, dilo — es mejor honestidad metodológica que una explicación inventada)

**Solución aplicada:** (código/comandos exactos que lo resolvieron)

**Tiempo perdido:**

**Nota para la tesis:** (si este incidente aporta algo al argumento de la tesis, ej. evidencia de complejidad de integración con sistemas legacy)
```
