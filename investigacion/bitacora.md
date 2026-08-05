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
