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
