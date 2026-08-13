"""
NAILA - Adapter / API Facade para osCommerce
Expone operaciones simples que el Agente LLM puede invocar mediante tool calling,
delegando la traducción real hacia el ACL.
"""

from oscommerce_acl import OsCommerceACL


class OsCommerceAdapter:
    def __init__(self):
        self.acl = OsCommerceACL()

    def list_available_products(self, limit=10):
        """
        Operación expuesta al Agente LLM.
        No expone detalles del esquema de osCommerce ni de SQL - solo un resultado limpio.
        """
        products = self.acl.get_available_products(limit=limit)
        return {
            "count": len(products),
            "products": products,
        }


# Definición del "tool" en formato compatible con Ollama function/tool calling
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "list_available_products",
        "description": "Lista los productos actualmente disponibles en la tienda osCommerce, con su precio y stock.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Número máximo de productos a devolver",
                }
            },
            "required": [],
        },
    },
}
