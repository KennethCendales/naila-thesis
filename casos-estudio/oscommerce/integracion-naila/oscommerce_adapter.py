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

    def search_products_by_name(self, keyword, limit=10):
        """
        Operación expuesta al Agente LLM para búsqueda de productos por nombre.
        """
        products = self.acl.search_products_by_name(keyword=keyword, limit=limit)
        return {
            "count": len(products),
            "products": products,
        }

    def get_order_status(self, order_id):
        """
        Operación expuesta al Agente LLM para consultar el estado de un pedido.
        """
        order = self.acl.get_order_status(order_id=order_id)
        if order is None:
            return {"found": False, "message": f"No se encontró el pedido #{order_id}"}
        return {"found": True, "order": order}


# Definición de los "tools" en formato compatible con Ollama function/tool calling
TOOL_DEFINITIONS = [
    {
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
    },
    {
        "type": "function",
        "function": {
            "name": "search_products_by_name",
            "description": "Busca productos en la tienda osCommerce cuyo nombre contenga una palabra clave.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Palabra clave a buscar en el nombre del producto",
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
            "name": "get_order_status",
            "description": "Consulta el estado y detalles de un pedido específico de osCommerce dado su número de orden.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "Número de identificación del pedido",
                    }
                },
                "required": ["order_id"],
            },
        },
    },
]
