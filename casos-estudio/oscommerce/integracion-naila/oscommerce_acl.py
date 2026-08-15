"""
NAILA - Anti-Corruption Layer para osCommerce
Traduce entre el modelo canónico de NAILA y el esquema real de la base de datos de osCommerce v2.3.4.
Acceso de solo lectura en esta primera versión (Día 14).
"""

import pymysql


class OsCommerceACL:
    def __init__(self, host="localhost", port=3306, user="oscommerce", password="oscommerce", database="oscommerce"):
        self.connection_params = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "cursorclass": pymysql.cursors.DictCursor,
        }

    def _connect(self):
        return pymysql.connect(**self.connection_params)

    def get_available_products(self, limit=10):
        """
        Traduce la intención canónica 'listar productos disponibles'
        hacia la tabla real de osCommerce: products.
        Devuelve una lista de diccionarios en formato canónico NAILA,
        no en el formato crudo de la tabla osCommerce.
        """
        query = """
            SELECT products_id, products_model, products_price, products_quantity
            FROM products
            WHERE products_status = 1
            ORDER BY products_id
            LIMIT %s
        """
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (limit,))
                raw_results = cursor.fetchall()
        finally:
            connection.close()

        # Traducción hacia el modelo canónico de NAILA
        canonical_products = [
            {
                "id": row["products_id"],
                "model": row["products_model"],
                "price": float(row["products_price"]),
                "stock": row["products_quantity"],
            }
            for row in raw_results
        ]
        return canonical_products

    def search_products_by_name(self, keyword, limit=10):
        """
        Traduce la intención canónica 'buscar producto por nombre'
        hacia las tablas products + products_description de osCommerce
        (el nombre del producto vive en una tabla separada, no en 'products').
        """
        query = """
            SELECT p.products_id, p.products_model, p.products_price, p.products_quantity,
                   pd.products_name
            FROM products p
            JOIN products_description pd ON p.products_id = pd.products_id
            WHERE pd.products_name LIKE %s
              AND p.products_status = 1
              AND pd.language_id = 1
            ORDER BY p.products_id
            LIMIT %s
        """
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (f"%{keyword}%", limit))
                raw_results = cursor.fetchall()
        finally:
            connection.close()

        return [
            {
                "id": row["products_id"],
                "name": row["products_name"],
                "model": row["products_model"],
                "price": float(row["products_price"]),
                "stock": row["products_quantity"],
            }
            for row in raw_results
        ]

    def get_order_status(self, order_id):
        """
        Traduce la intención canónica 'consultar estado de un pedido'
        hacia las tablas orders + orders_total de osCommerce.
        Nota: osCommerce no almacena el total en 'orders' directamente;
        lo normaliza en 'orders_total', con una fila por concepto
        (subtotal, envío, impuestos, total), identificada por 'class'.
        """
        order_query = """
            SELECT orders_id, customers_name, date_purchased, orders_status
            FROM orders
            WHERE orders_id = %s
        """
        total_query = """
            SELECT value
            FROM orders_total
            WHERE orders_id = %s AND class = 'ot_total'
        """
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(order_query, (order_id,))
                row = cursor.fetchone()

                if row is None:
                    return None

                cursor.execute(total_query, (order_id,))
                total_row = cursor.fetchone()
        finally:
            connection.close()

        return {
            "order_id": row["orders_id"],
            "customer_name": row["customers_name"],
            "date": str(row["date_purchased"]),
            "status_id": row["orders_status"],
            "total": float(total_row["value"]) if total_row else None,
        }

