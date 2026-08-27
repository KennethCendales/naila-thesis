"""
NAILA - Demostración ilustrativa (NO forma parte del experimento medido)

Mismo propósito que oscommerce_acl_generico_ejemplo.py: demuestra que TracACL
también puede implementar formalmente el contrato de BaseACL, evidenciando
que naila_core.py no fue diseñado a la medida de un solo sistema legacy.

ADVERTENCIA METODOLÓGICA: ver oscommerce_acl_generico_ejemplo.py para el
detalle completo de por qué este archivo es ilustrativo y no forma parte de
la medición empírica formal reportada en la tesis.
"""

import sys
import os
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from naila_core import BaseACL


class TracACLGenerico(BaseACL):
    """Versión ilustrativa de TracACL, implementando formalmente BaseACL."""

    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_open_tickets(self, limit=20):
        query = """
            SELECT id, summary, type, priority, status
            FROM ticket WHERE status != 'closed' ORDER BY id LIMIT ?
        """
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query, (limit,))
            columns = [desc[0] for desc in cursor.description]
            raw_results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        # Mismo helper genérico usado por OsCommerceACLGenerico - evidencia
        # de que to_canonical() es reutilizable entre dominios completamente
        # distintos (e-commerce vs. gestión de proyectos)
        field_mapping = {
            "id": "id", "summary": "summary",
            "type": "type", "priority": "priority", "status": "status",
        }
        return [self.to_canonical(row, field_mapping) for row in raw_results]
