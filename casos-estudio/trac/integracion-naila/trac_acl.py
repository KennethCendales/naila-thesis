"""
NAILA - Anti-Corruption Layer para Trac
Traduce entre el modelo canónico de NAILA y el esquema real de la base de datos SQLite de Trac.
Acceso de solo lectura en esta primera versión (Día 18).
"""

import sqlite3
import os


class TracACL:
    def __init__(self, db_path=None):
        if db_path is None:
            # Ruta relativa por defecto: asume que este archivo vive en
            # casos-estudio/trac/integracion-naila/, y la BD en casos-estudio/trac/data/db/trac.db
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "..", "data", "db", "trac.db")
        self.db_path = os.path.normpath(db_path)

    def _connect(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"No se encontró la base de datos de Trac en: {self.db_path}. "
                "Verifica que el volumen de Docker esté montado correctamente."
            )
        return sqlite3.connect(self.db_path)

    def get_open_tickets(self, limit=20):
        """
        Traduce la intención canónica 'listar tickets abiertos'
        hacia la tabla real de Trac: ticket.
        Devuelve una lista en formato canónico NAILA, no en el formato crudo de Trac.
        """
        query = """
            SELECT id, summary, type, priority, status
            FROM ticket
            WHERE status != 'closed'
            ORDER BY id
            LIMIT ?
        """
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query, (limit,))
            columns = [desc[0] for desc in cursor.description]
            raw_results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        # Traducción hacia el modelo canónico de NAILA
        canonical_tickets = [
            {
                "id": row["id"],
                "summary": row["summary"],
                "type": row["type"],
                "priority": row["priority"],
                "status": row["status"],
            }
            for row in raw_results
        ]
        return canonical_tickets
