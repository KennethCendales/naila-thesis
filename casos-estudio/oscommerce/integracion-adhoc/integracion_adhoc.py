"""
NAILA - Version AD HOC (baseline sin patron arquitectonico) para osCommerce.
Resuelve los mismos 3 casos de uso que integracion-naila, pero sin separar
Adapter y Anti-Corruption Layer: todo mezclado en funciones sueltas, con SQL
embebido directamente. Representa como se integraria un agente LLM sin
disciplina arquitectonica - rapido, funcional, pero sin separacion de
responsabilidades. Usado como baseline de comparacion contra NAILA.
"""

import pymysql


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="oscommerce",
        password="oscommerce",
        database="oscommerce",
        cursorclass=pymysql.cursors.DictCursor,
    )


def list_available_products(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT products_id, products_model, products_price, products_quantity FROM products WHERE products_status = 1 ORDER BY products_id LIMIT %s",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    products = []
    for row in rows:
        products.append({
            "id": row["products_id"],
            "model": row["products_model"],
            "price": float(row["products_price"]),
            "stock": row["products_quantity"],
        })
    return {"count": len(products), "products": products}


def search_products_by_name(keyword, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT p.products_id, p.products_model, p.products_price, p.products_quantity, pd.products_name FROM products p JOIN products_description pd ON p.products_id = pd.products_id WHERE pd.products_name LIKE %s AND p.products_status = 1 AND pd.language_id = 1 ORDER BY p.products_id LIMIT %s",
        (f"%{keyword}%", limit),
    )
    rows = cursor.fetchall()
    conn.close()
    products = []
    for row in rows:
        products.append({
            "id": row["products_id"],
            "name": row["products_name"],
            "model": row["products_model"],
            "price": float(row["products_price"]),
            "stock": row["products_quantity"],
        })
    return {"count": len(products), "products": products}


def get_order_status(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT orders_id, customers_name, date_purchased, orders_status FROM orders WHERE orders_id = %s",
        (order_id,),
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return {"found": False, "message": f"No se encontró el pedido #{order_id}"}
    cursor.execute(
        "SELECT value FROM orders_total WHERE orders_id = %s AND class = 'ot_total'",
        (order_id,),
    )
    total_row = cursor.fetchone()
    conn.close()
    return {
        "found": True,
        "order": {
            "order_id": row["orders_id"],
            "customer_name": row["customers_name"],
            "date": str(row["date_purchased"]),
            "status_id": row["orders_status"],
            "total": float(total_row["value"]) if total_row else None,
        },
    }


# Tool definitions (formato Ollama), mezcladas en el mismo archivo sin separación
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_available_products",
            "description": "Lista los productos actualmente disponibles en la tienda osCommerce, con su precio y stock.",
            "parameters": {
                "type": "object",
                "properties": {"limit": {"type": "integer", "description": "Número máximo de productos a devolver"}},
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
                    "keyword": {"type": "string", "description": "Palabra clave a buscar en el nombre del producto"},
                    "limit": {"type": "integer", "description": "Número máximo de resultados a devolver"},
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
                "properties": {"order_id": {"type": "integer", "description": "Número de identificación del pedido"}},
                "required": ["order_id"],
            },
        },
    },
]
