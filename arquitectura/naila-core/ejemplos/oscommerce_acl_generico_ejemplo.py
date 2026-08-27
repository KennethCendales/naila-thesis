"""
NAILA - Demostración ilustrativa (NO forma parte del experimento medido)

Este archivo muestra cómo la implementación de osCommerce PODRÍA reescribirse
para implementar formalmente el contrato de naila_core.BaseACL, como evidencia
de que el patrón arquitectónico es genuinamente reutilizable entre sistemas
legacy distintos.

ADVERTENCIA METODOLÓGICA: este archivo es ilustrativo únicamente. Las métricas
de mantenibilidad y rendimiento reportadas en la tesis (Fases 4 y 5) fueron
calculadas sobre la versión original en
casos-estudio/oscommerce/integracion-naila/oscommerce_acl.py, que NO fue
modificada. Este archivo NO se incluye en la medición empírica formal.
"""

import sys
import os
import pymysql

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from naila_core import BaseACL


class OsCommerceACLGenerico(BaseACL):
    """Versión ilustrativa de OsCommerceACL, implementando formalmente BaseACL."""

    def __init__(self, host="localhost", port=3306, user="oscommerce", password="oscommerce", database="oscommerce"):
        self.connection_params = {
            "host": host, "port": port, "user": user,
            "password": password, "database": database,
            "cursorclass": pymysql.cursors.DictCursor,
        }

    def _connect(self):
        return pymysql.connect(**self.connection_params)

    def get_available_products(self, limit=10):
        query = """
            SELECT products_id, products_model, products_price, products_quantity
            FROM products WHERE products_status = 1 ORDER BY products_id LIMIT %s
        """
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (limit,))
                raw_results = cursor.fetchall()
        finally:
            connection.close()

        # Uso del helper genérico heredado de BaseACL, en vez de reescribir
        # manualmente la construcción del diccionario canónico en cada método
        field_mapping = {
            "id": "products_id", "model": "products_model",
            "price": "products_price", "stock": "products_quantity",
        }
        return [self.to_canonical(row, field_mapping) for row in raw_results]
