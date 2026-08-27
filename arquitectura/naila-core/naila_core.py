"""
NAILA - Núcleo genérico (naila_core)

Define el contrato abstracto que cualquier implementación concreta de NAILA
debe seguir, independientemente del sistema legacy al que se aplique.

IMPORTANTE - Nota metodológica: estas clases NO reemplazan ni modifican las
implementaciones ya medidas empíricamente en las Fases 4 y 5 del proyecto
(oscommerce_acl.py, trac_acl.py, y sus respectivos adapters). Se presentan
como una extensión conceptual que demuestra la generalizabilidad del patrón
arquitectónico, ilustrada mediante ejemplos separados en /ejemplos, sin
alterar los artefactos de código sobre los que se reportan las métricas
formales de la tesis.
"""

from abc import ABC, abstractmethod


class BaseACL(ABC):
    """
    Contrato genérico para una Anti-Corruption Layer.

    Cualquier ACL concreta debe:
    1. Implementar _connect(), estableciendo la conexión con el mecanismo
       de persistencia específico del sistema legacy (base de datos,
       archivo, o cualquier otro medio).
    2. Usar to_canonical() para traducir filas/registros crudos del legacy
       hacia el modelo canónico de NAILA, evitando que cada implementación
       reescriba manualmente esta lógica de mapeo.
    """

    @abstractmethod
    def _connect(self):
        """Establece la conexión con el mecanismo de persistencia del sistema legacy."""
        raise NotImplementedError

    @staticmethod
    def to_canonical(raw_row: dict, field_mapping: dict) -> dict:
        """
        Traduce una fila cruda del sistema legacy a un diccionario canónico.

        field_mapping: diccionario {clave_canonica: clave_en_el_legacy}
        Ejemplo: {"id": "products_id", "price": "products_price"}
        """
        return {
            canonical_key: raw_row.get(raw_key)
            for canonical_key, raw_key in field_mapping.items()
        }


class BaseAdapter(ABC):
    """
    Contrato genérico para un Adapter / API Facade.

    Cualquier Adapter concreto debe:
    1. Recibir una instancia de una subclase de BaseACL en su constructor.
    2. Declarar tool_definitions, la lista de herramientas (en el formato
       de tool-calling del proveedor de LLM usado) que este Adapter expone
       al agente de IA generativa.
    """

    def __init__(self, acl: BaseACL):
        self.acl = acl

    @property
    @abstractmethod
    def tool_definitions(self) -> list:
        """Debe devolver la lista de definiciones de herramientas expuestas al agente LLM."""
        raise NotImplementedError
