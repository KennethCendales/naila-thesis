"""
NAILA - Adapter / API Facade para Trac
Expone operaciones simples que el Agente LLM puede invocar mediante tool calling,
delegando la traducción real hacia el ACL.
"""

from trac_acl import TracACL


class TracAdapter:
    def __init__(self):
        self.acl = TracACL()

    def list_open_tickets(self, limit=20):
        """
        Operación expuesta al Agente LLM.
        No expone detalles del esquema de Trac ni de SQL - solo un resultado limpio.
        """
        tickets = self.acl.get_open_tickets(limit=limit)
        return {
            "count": len(tickets),
            "tickets": tickets,
        }

    def search_tickets_by_keyword(self, keyword, limit=20):
        """
        Operación expuesta al Agente LLM para búsqueda de tickets por palabra clave.
        """
        tickets = self.acl.search_tickets_by_keyword(keyword=keyword, limit=limit)
        return {
            "count": len(tickets),
            "tickets": tickets,
        }

    def get_ticket_details(self, ticket_id):
        """
        Operación expuesta al Agente LLM para consultar detalles completos de un ticket.
        """
        ticket = self.acl.get_ticket_details(ticket_id=ticket_id)
        if ticket is None:
            return {"found": False, "message": f"No se encontró el ticket #{ticket_id}"}
        return {"found": True, "ticket": ticket}


# Definición de los "tools" en formato compatible con Ollama function/tool calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_open_tickets",
            "description": "Lista los tickets actualmente abiertos (no cerrados) en el proyecto Trac, con su tipo, prioridad y estado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Número máximo de tickets a devolver",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_tickets_by_keyword",
            "description": "Busca tickets en Trac cuyo resumen (summary) contenga una palabra clave.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Palabra clave a buscar en el resumen del ticket",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Número máximo de resultados a devolver",
                    },
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
                "properties": {
                    "ticket_id": {
                        "type": "integer",
                        "description": "Número de identificación del ticket",
                    }
                },
                "required": ["ticket_id"],
            },
        },
    },
]
