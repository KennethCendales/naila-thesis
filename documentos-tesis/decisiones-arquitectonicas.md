# Registro de Decisiones Arquitectónicas (ADR) — NAILA

> Formato ADR (Architecture Decision Record): estándar de la industria para documentar decisiones técnicas importantes con su contexto, alternativas consideradas y justificación. Cada decisión relevante del proyecto debe quedar aquí, no solo en la bitácora diaria — esto es lo que un jurado revisa para evaluar el rigor de tus decisiones técnicas.

---

## ADR-001 — Ubicación del proyecto fuera de OneDrive

**Fecha:** 3/8/2026
**Estado:** Aceptada

**Contexto:** El proyecto se creó inicialmente en `C:\Users\kenneth\OneDrive\Documentos\naila-thesis`.

**Problema:** OneDrive sincroniza automáticamente archivos, lo que genera conflictos conocidos con Git (bloqueos tipo `index.lock`) y con Docker (rendimiento degradado en volúmenes montados, sincronización innecesaria de artefactos pesados generados por contenedores).

**Decisión:** Mover el proyecto a `C:\Users\kenneth\Documents\naila-thesis`, fuera del árbol sincronizado por OneDrive.

**Alternativas consideradas:** Mantener en OneDrive y pausar la sincronización de esa carpeta específica — descartada por mayor complejidad de configuración y riesgo de reactivación accidental.

**Consecuencias:** Se pierde respaldo automático en la nube vía OneDrive; se mitiga usando GitHub como respaldo remoto principal del código (no así de artefactos generados como bases de datos locales).

---

## ADR-002 — Versión de MySQL: 5.6 en vez de 5.7

**Fecha:** 4/8/2026
**Estado:** Aceptada — pendiente de verificación formal de causa raíz

**Contexto:** Se requiere un servidor MySQL para osCommerce v2.3.4, que usa las extensiones legacy `mysql` y `mysqli` de PHP 5.6.

**Problema observado:** Al usar `mysql:5.7` como imagen de base de datos, la conexión desde el contenedor `web` fallaba con error de conexión rechazada / "can't connect to MySQL server".

**Hipótesis de causa raíz:** Posible incompatibilidad de protocolo/autenticación entre el driver legacy `ext/mysql` de PHP 5.6 (deprecado, removido en PHP 7) y cambios internos de MySQL 5.7. *(Nota metodológica: esto es una hipótesis razonada, no una causa confirmada — si el tiempo lo permite, vale la pena verificarla formalmente con los logs exactos del contenedor `db` para el documento final de tesis, ya que "connection refused" también puede deberse a timing de arranque del contenedor).*

**Decisión:** Usar `mysql:5.6` como imagen de base de datos, versión contemporánea a la época de osCommerce v2.3.4 (2014).

**Alternativas consideradas:**
- Mantener MySQL 5.7 e investigar configuración de compatibilidad — descartada por tiempo, dado que 5.6 es la opción "históricamente correcta" para este legacy.
- Usar MariaDB como alternativa — no explorada.

**Consecuencias:** Mayor coherencia histórica del entorno (MySQL 5.6 es contemporáneo a osCommerce 2.3.4), pero introduce una imagen Docker también antigua, con sus propios posibles problemas de disponibilidad de paquetes a futuro.

---

## ADR-003 — Dockerfile personalizado con repositorios Debian archivados

**Fecha:** 4/8/2026
**Estado:** Aceptada

**Contexto:** La imagen base `php:5.6-apache` no incluye las extensiones PHP requeridas por osCommerce (`mysql`, `mysqli`, `gd`).

**Problema:** Al intentar instalar estas extensiones vía `apt-get install`, los repositorios Debian por defecto de la imagen ya no están activos (paquetes movidos a `archive.debian.org`), causando fallos de `apt-get update`.

**Decisión:** Crear un `Dockerfile` personalizado que:
1. Redirige las fuentes APT hacia `archive.debian.org`
2. Desactiva la verificación `Check-Valid-Until` (los repos archivados no se actualizan, por lo que su fecha de "válido hasta" ya expiró)
3. Instala paquetes con `--allow-insecure-repositories --allow-unauthenticated`
4. Compila e instala las extensiones `gd`, `mysql`, `mysqli`

**Alternativas consideradas:** Usar una imagen PHP más moderna con compatibilidad retroactiva — descartada porque introduciría diferencias de comportamiento respecto al entorno original de 2014, contaminando la validez del caso de estudio como "legacy real".

**Consecuencias:** El entorno de desarrollo depende de que `archive.debian.org` siga disponible a futuro — riesgo menor pero real de reproducibilidad a largo plazo. Vale la pena documentar la versión exacta de la imagen usada (`php:5.6-apache`, digest si es posible) para máxima reproducibilidad en la tesis.

---

## ADR-004 — Autenticación HTTP Basic adicional sobre el panel de administración

**Fecha:** 4/8/2026
**Estado:** Aceptada

**Contexto:** El propio módulo de "Security Checks" de osCommerce señaló como advertencia (no crítica) la ausencia de una capa de autenticación HTTP a nivel de servidor web (Apache) sobre la carpeta `/admin`, adicional al login propio de la aplicación.

**Problema:** El panel de administración solo dependía de un único mecanismo de autenticación (el login de la aplicación PHP), sin capa adicional de defensa en profundidad.

**Decisión:** Configurar autenticación HTTP Basic vía Apache (`.htaccess` + `.htpasswd`) sobre la carpeta `/admin`, exigiendo una segunda credencial (independiente del login de osCommerce) antes de poder acceder al panel.

**Alternativas consideradas:**
- No implementarla, dado que la seguridad no es una métrica central evaluada en esta tesis (se definió explícitamente fuera del alcance en la fase de diseño metodológico) — descartada porque, aunque no se mide formalmente, es una buena práctica de bajo costo que mejora el realismo del entorno de caso de estudio (un sistema en producción real normalmente tendría esta capa).

**Consecuencias:**
- Requiere habilitar `AllowOverride All` en la configuración de Apache dentro del `Dockerfile`, lo cual amplía el alcance de lo que un `.htaccess` puede sobrescribir — aceptable en este entorno de desarrollo controlado, pero a documentar como configuración no necesariamente apta para producción sin revisión adicional.
- Introduce una credencial adicional que debe gestionarse por separado del login de la aplicación (ver `.gitignore` del proyecto, que ya excluye `configure.php`; el `.htpasswd` generado también debe tratarse como sensible y no versionarse).

---

## ADR-005 — Permisos de creación de tickets otorgados a usuario anónimo en Trac

**Fecha:** 5/8/2026
**Estado:** Aceptada

**Contexto:** Por configuración por defecto, Trac restringe la creación y modificación de tickets a usuarios autenticados. El entorno `tracd` levantado para el caso de estudio no tiene un sistema de autenticación configurado (no se implementó login de usuarios).

**Problema:** Al intentar crear tickets de prueba (necesarios como dataset para las pruebas del agente de IA), el sistema devolvió `Error: Forbidden — TICKET_CREATE privileges are required`.

**Decisión:** Otorgar los permisos `TICKET_CREATE`, `TICKET_MODIFY` y `TICKET_VIEW` al usuario `anonymous` mediante `trac-admin permission add`, en vez de configurar un sistema de autenticación completo (usuario/contraseña).

**Alternativas consideradas:**
- Configurar autenticación real (HTTP Basic Auth o `htdigest`) con un usuario administrador dedicado — descartada por no ser prioritaria: Trac, a diferencia de osCommerce, no fue seleccionado para evaluar seguridad, y el entorno es exclusivamente de prueba/desarrollo local, sin exposición pública.

**Consecuencias:**
- El entorno de Trac queda con permisos más permisivos que un despliegue real de producción — aceptable dado que el alcance de la tesis no incluye seguridad como variable evaluada (ver definición de alcance en el objetivo general).
- Si en fases posteriores el agente de IA necesita simular acciones "como un usuario específico" (por ejemplo, para medir trazabilidad de quién ejecuta una acción), esta decisión tendría que revisarse — anotar como posible ajuste futuro si surge esa necesidad al diseñar la capa de integración (Fase 3 del plan de trabajo).

---

## Plantilla para futuras decisiones

```markdown
## ADR-00N — [Título corto de la decisión]

**Fecha:**
**Estado:** Propuesta / Aceptada / Rechazada / Reemplazada por ADR-XXX

**Contexto:** (¿Qué situación obliga a decidir?)

**Problema:** (¿Qué está fallando o qué hay que resolver?)

**Decisión:** (¿Qué se decidió hacer?)

**Alternativas consideradas:** (¿Qué otras opciones se evaluaron y por qué se descartaron?)

**Consecuencias:** (¿Qué implicaciones tiene esta decisión a futuro?)
```
