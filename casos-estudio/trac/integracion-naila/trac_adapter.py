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


# Definición del "tool" en formato compatible con Ollama function/tool calling
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
]
