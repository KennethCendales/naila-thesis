# NAILA — Demo funcional

Chat con IA generativa integrado sobre un sistema legacy real (osCommerce v2.3.4), construido para validar de forma tangible la arquitectura de investigación **NAILA (Non-Invasive Architecture for Integrating LLM Agents)**.

> Este demo es una prueba de concepto local — no un producto en producción. Ver `documentos-tesis/decisiones-arquitectonicas.md` (ADR-008) para el alcance exacto y por qué no incluye, todavía, un piloto en un entorno real.

## Qué hace

Un visitante de una tienda (simulada) puede preguntarle al asistente, en lenguaje natural, por productos disponibles o el estado de un pedido. El asistente:
1. Interpreta la intención con un modelo de lenguaje (Qwen3.5-9B, corriendo localmente vía Ollama)
2. Consulta datos reales del sistema legacy a través de la arquitectura NAILA (Adapter + Anti-Corruption Layer) — el mismo código validado empíricamente en la tesis, sin modificaciones
3. Redacta una respuesta breve, en lista, con links reales a la página del producto en osCommerce

## Stack técnico

| Componente | Tecnología |
|---|---|
| Backend | Python, FastAPI |
| Modelo de lenguaje | Qwen3.5-9B, local, vía Ollama |
| Sistema legacy | osCommerce v2.3.4 (PHP/MySQL), en Docker |
| Frontend | HTML/CSS/JS vanilla, sin frameworks |
| Arquitectura de integración | NAILA — Anti-Corruption Layer + Adapter (ver `casos-estudio/oscommerce/integracion-naila/`) |

## Cómo levantarlo

### Opción A — Con Docker (recomendado, un solo comando)

Requisitos previos: Docker Desktop, Ollama con `qwen3.5:9b` descargado, osCommerce corriendo.

```powershell
# 1. Levantar osCommerce (si no está corriendo)
cd casos-estudio/oscommerce
docker-compose up -d

# 2. Levantar el demo completo (backend + frontend)
cd ../../demo
docker-compose up --build
```

Listo. Abre `http://localhost:3000` en el navegador.

**Nota técnica:** el backend contenerizado se conecta a MySQL y a Ollama (que corren en tu máquina, fuera de Docker) mediante `host.docker.internal`, el nombre especial que Docker Desktop usa para referirse al host — no requiere que compartas redes entre proyectos de Docker distintos.

### Opción B — Ejecución nativa (sin Docker, para desarrollo/debug)

Requisitos previos: Docker Desktop (solo para osCommerce), Ollama con `qwen3.5:9b` descargado, Python 3.11+.

```powershell
# 1. Levantar osCommerce (si no está corriendo)
cd casos-estudio/oscommerce
docker-compose up -d

# 2. Levantar el backend del demo
cd ../../demo/backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

# 3. Abrir el frontend
# Simplemente abre demo/frontend/index.html en el navegador
```

Verifica que todo esté arriba:
- `http://localhost:8080` → tienda osCommerce
- `http://localhost:8000/health` → debe responder `{"status": "ok"}`
- `ollama list` → debe incluir `qwen3.5:9b`

## Ejemplos de uso

- "¿qué productos tienen disponibles?"
- "busca productos que tengan Weapon en el nombre"
- "¿cuál es el estado del pedido número 1?"

## Por qué existe este demo

Este proyecto nació como una tesis de investigación empírica en Ingeniería de Software, que compara arquitectónicamente NAILA (con patrón ACL + Adapter) contra una integración ad hoc, midiendo mantenibilidad, esfuerzo y rendimiento sobre dos casos de estudio (osCommerce y Trac). Este demo es la evidencia de que el hallazgo de la investigación —una arquitectura de integración no invasiva— es aplicable a un caso de uso real y reconocible, no solo una abstracción teórica.

La contribución académica no es "el chat" (una capacidad ya comercialmente disponible), sino el patrón arquitectónico validado empíricamente y su trade-off cuantificado — ver `documentos-tesis/discusion-tesis.md`, Sección 8, para la distinción completa.

## Limitaciones conocidas de este demo

- Corre en `localhost`, sin autenticación ni HTTPS — no apto para exposición pública tal cual
- El modelo local (Qwen3.5-9B) puede, ocasionalmente, no seguir el formato de respuesta solicitado (limitación de confiabilidad de salida estructurada en modelos pequeños, documentada en la investigación)
- Solo soporta operaciones de lectura (consultar productos, pedidos y políticas) — no escritura (crear/modificar)
- **No es un producto "instalable en cualquier negocio sin código"**: el empaquetado Docker facilita el despliegue de *este* demo específico (osCommerce), pero cada nuevo sistema legacy requiere escribir su propia ACL/Adapter siguiendo el patrón NAILA (ver `documentos-tesis/guia-generalizacion-naila.md`) — no es una integración sin código, es un patrón arquitectónico reutilizable que reduce el esfuerzo de esa integración, no lo elimina

## Autor

Kenneth Cendales — Ingeniería de Software, Universidad Manuela Beltrán
