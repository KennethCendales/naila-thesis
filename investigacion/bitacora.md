# Bitácora Diaria — NAILA

> Registro cronológico de avance. Completar al final de cada sesión de trabajo, mientras el contexto está fresco (no dejar para después).

---

## Día 1 — 3/8/2026

**Objetivo del día:** Configurar entorno de trabajo (repositorio + estructura + Docker)

**Tareas realizadas:**
- Creación de estructura de carpetas del proyecto (`investigacion`, `arquitectura`, `casos-estudio/oscommerce`, `casos-estudio/trac`, `metricas`, `documentos-tesis`)
- Inicialización de repositorio Git local
- Conexión a repositorio remoto privado en GitHub (`KennethCendales/naila-thesis`)
- Verificación de Docker Desktop (`docker run hello-world` exitoso)

**Decisiones tomadas:**
- Proyecto movido de `OneDrive` a `C:\Users\kenneth\Documents\naila-thesis` — ver detalle en `incidentes-tecnicos.md` #001
- Rama principal del repositorio: `master` (no `main`)

**Tiempo invertido:** ~2 horas (estimado, ajustar si tienes el dato real)

**Estado:** ✅ Completado

---

## Día 2 — 4/8/2026

**Objetivo del día:** Levantar osCommerce V2.3.4 en Docker

**Tareas realizadas:**
- Clonado del repositorio oficial `osCommerce/oscommerce2`, tag `v2.3.4`
- Identificación de que el punto de entrada real (`index.php`) está en `/catalog`, no en la raíz del repo
- Construcción de `Dockerfile` personalizado sobre `php:5.6-apache` para instalar extensiones `mysql`, `mysqli`, `gd`
- Resolución de fallo de repositorios APT (Debian) — ver `incidentes-tecnicos.md` #002
- Resolución de incompatibilidad MySQL 5.7 → downgrade a MySQL 5.6 — ver `incidentes-tecnicos.md` #003
- Instalación exitosa del wizard de osCommerce (Server Capabilities: todo en verde)

**Decisiones tomadas:**
- Imagen de base de datos: `mysql:5.6` (no 5.7) — justificación completa en ADR-002
- Volumen montado apunta a `./catalog` en vez de raíz del proyecto
- `sql_mode` relajado a `NO_ENGINE_SUBSTITUTION` para permitir el esquema legacy — ver Incidente #004
- Se agregó autenticación HTTP Basic (Apache) sobre `/admin`, como capa adicional de seguridad no obligatoria — ver ADR-004

**Tareas adicionales realizadas (segunda parte del día):**
- Configuración completa de la tienda ficticia "Pola Store" vía wizard
- Verificación de credenciales excluidas correctamente del control de versiones (`.gitignore` propio de osCommerce, ya cubría `configure.php`)
- Eliminación de la carpeta `/install` (requisito de seguridad post-instalación)
- Resolución de advertencia `customers_dob` (sql_mode estricto)
- Configuración de HTTP Basic Auth sobre el panel de administración
- Todos los "Security Checks" de osCommerce en verde, salvo "Version Check" (no aplicable en entorno local sin salida a internet para ese fin)

**Tiempo invertido:** ~3-4 horas (incluye instalación base + troubleshooting + configuración de tienda + seguridad)

**Estado:** ✅ Completado

---

## Día 3 — 5/8/2026

**Objetivo del día:** Levantar Trac en Docker (segundo caso de estudio)

**Tareas realizadas:**
- Construcción de `Dockerfile` sobre `python:3.11-slim`, instalación de Trac vía pip
- Creación de `docker-compose.yml` (SQLite embebido, sin contenedor de base de datos separado)
- Inicialización del entorno con `trac-admin initenv` — proyecto nombrado "NAILA - Trac Case Study"
- Contenedor `trac-trac-1` corriendo correctamente, interfaz web accesible en `http://localhost:8000/myproject`
- Otorgamiento de permisos `TICKET_CREATE`, `TICKET_MODIFY`, `TICKET_VIEW` al usuario anónimo — ver Incidente #005 / ADR-005
- Creación de 4 tickets de prueba con variedad de tipo, prioridad y estado (dataset para pruebas futuras del agente)

**Decisiones tomadas:**
- Base de datos: SQLite por defecto (no MySQL/PostgreSQL) — suficiente para el caso de estudio, sin necesidad de contenedor adicional
- Permisos de `anonymous` ampliados en vez de configurar autenticación completa — ver ADR-005

**Hallazgo relevante:** A diferencia de osCommerce (Día 2), Trac migró su motor de templates de Genshi a Jinja2 y su compatibilidad a Python 3.5+, lo que redujo significativamente la fricción de instalación — buen dato comparativo para la discusión de resultados (no todos los sistemas "legacy" tienen el mismo nivel de deuda técnica de infraestructura).

**Tiempo invertido:** < 1 hora

**Estado:** ✅ Completado

---

## Día 14 — Prototipo mínimo: Adapter para osCommerce (Fase 2)

**Objetivo del día:** Primera implementación funcional del Adapter sobre osCommerce — hito central del proyecto.

**Tareas realizadas:**
- Configuración de entorno Python (venv) dentro de `casos-estudio/oscommerce/integracion-naila/`
- Instalación de Ollama, descarga y verificación de Qwen3.5-9B
- Implementación de `OsCommerceACL` — traduce entre modelo canónico NAILA y esquema real de osCommerce (tabla `products`), acceso de solo lectura vía `pymysql`
- Implementación de `OsCommerceAdapter` — expone `list_available_products()` como tool para el agente, oculta detalles de SQL/esquema
- Script `test_flujo_completo.py` — primera prueba end-to-end exitosa

**Resultado:** ✅ **Flujo completo funcionando de punta a punta**: "muéstrame los productos disponibles" (lenguaje natural) → Qwen3.5-9B reconoce la intención → invoca `list_available_products` → Adapter delega al ACL → ACL traduce hacia SQL real sobre `products` → osCommerce devuelve datos reales de "Pola Store" (10 productos, con id/model/price/stock) → respuesta canónica limpia, sin exponer el esquema interno de osCommerce.

**Decisiones tomadas:**
- Punto de integración con osCommerce: consulta directa a MySQL en modo solo lectura (osCommerce no expone API REST nativa) — coherente con la práctica de "empezar con acceso de solo lectura" identificada en el estado del arte (Día 6, fuente #8).
- Estructura de clases (`OsCommerceACL`, `OsCommerceAdapter`) alineada con la definición operacional de "capa de integración" del Día 12 — código propio, orientado a objetos, medible con CBO/complejidad ciclomática.

**Tiempo invertido:** ~2 horas (incluye instalación de Ollama + descarga del modelo + implementación del prototipo)

**Estado:** ✅ Completado — primer caso de uso funcional de NAILA

---

## Plantilla para los próximos días

```markdown
## Día N — [fecha]

**Objetivo del día:**

**Tareas realizadas:**
-

**Decisiones tomadas:**
-

**Problemas encontrados:** (si aplica, referenciar número de incidente en incidentes-tecnicos.md)
-

**Tiempo invertido:**

**Estado:** ✅ Completado / ⏳ En progreso / ❌ Bloqueado
```
