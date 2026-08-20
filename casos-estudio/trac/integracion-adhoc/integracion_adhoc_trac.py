"""
NAILA - Version AD HOC (baseline sin patron arquitectonico) para Trac.
Resuelve los mismos 3 casos de uso que integracion-naila, pero sin separar
Adapter y Anti-Corruption Layer: todo mezclado en funciones sueltas, con SQL
embebido directamente. Usado como baseline de comparacion contra NAILA.
"""

import sqlite3
import os

DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "db", "trac.db")
)


def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"No se encontró la base de datos de Trac en: {DB_PATH}")
    return sqlite3.connect(DB_PATH)


def list_open_tickets(limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, summary, type, priority, status FROM ticket WHERE status != 'closed' ORDER BY id LIMIT ?",
        (limit,),
    )
    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    tickets = []
    for row in rows:
        tickets.append({
            "id": row["id"],
            "summary": row["summary"],
            "type": row["type"],
            "priority": row["priority"],
            "status": row["status"],
        })
    return {"count": len(tickets), "tickets": tickets}


def search_tickets_by_keyword(keyword, limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, summary, type, priority, status FROM ticket WHERE summary LIKE ? ORDER BY id LIMIT ?",
        (f"%{keyword}%", limit),
    )
    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    tickets = []
    for row in rows:
        tickets.append({
            "id": row["id"],
            "summary": row["summary"],
            "type": row["type"],
            "priority": row["priority"],
            "status": row["status"],
        })
    return {"count": len(tickets), "tickets": tickets}


def get_ticket_details(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, summary, description, type, priority, status, owner, reporter, component, milestone FROM ticket WHERE id = ?",
        (ticket_id,),
    )
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return {"found": False, "message": f"No se encontró el ticket #{ticket_id}"}
    data = dict(zip(columns, row))
    return {
        "found": True,
        "ticket": {
            "id": data["id"],
            "summary": data["summary"],
            "description": data["description"],
            "type": data["type"],
            "priority": data["priority"],
            "status": data["status"],
            "owner": data["owner"],
            "reporter": data["reporter"],
            "component": data["component"],
            "milestone": data["milestone"],
        },
    }


# Tool definitions (formato Ollama), mezcladas en el mismo archivo sin separación
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_open_tickets",
            "description": "Lista los tickets actualmente abiertos (no cerrados) en el proyecto Trac, con su tipo, prioridad y estado.",
            "parameters": {
                "type": "object",
                "properties": {"limit": {"type": "integer", "description": "Número máximo de tickets a devolver"}},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_tickets_by_keyword",
            "description": "Busca tickets en Trac cuyo resumen contenga una palabra clave.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "Palabra clave a buscar en el resumen del ticket"},
                    "limit": {"type": "integer", "description": "Número máximo de resultados a devolver"},
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket_details",
            "description": "Consulta los detalles completos de un ticket específico de Trac dado su número de identificación.",
            "parameters": {
                "type": "object",
                "properties": {"ticket_id": {"type": "integer", "description": "Número de identificación del ticket"}},
                "required": ["ticket_id"],
            },
        },
    },
]
