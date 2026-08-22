"""
NAILA - Calculador de CBO (Coupling Between Objects) - v3
Implementa la definición de Chidamber & Kemerer (1994): CBO(c) = número de
clases externas distintas a las que la clase c está acoplada.

v3 (Día 24, refinado): excluye módulos de utilidad genérica del sistema
operativo/lenguaje (os, sys) que no representan acoplamiento de diseño real,
sino manipulación incidental de rutas de archivos u otras operaciones de
sistema. Se mantiene la detección de módulos de acceso a datos/persistencia
(sqlite3, pymysql, etc.), ya que esos SÍ representan acoplamiento
arquitectónicamente significativo hacia el sistema legacy - es justamente lo
que esta métrica busca capturar en el contexto de NAILA.

Justificación de la exclusión (documentada en operacionalizacion-variables.md):
Chidamber & Kemerer definieron CBO pensando en acoplamiento entre clases del
dominio del problema, no en el uso de utilidades genéricas del lenguaje.
Contar 'os.path.join' como acoplamiento de diseño distorsiona la comparación
entre archivos que, por razones incidentales de implementación (ej. resolver
una ruta de archivo SQLite vs. conectar por host/puerto a MySQL), difieren en
su necesidad de manipular rutas, sin que eso refleje una diferencia real de
calidad arquitectónica.
"""

import ast
import sys as sys_module

# Módulos de utilidad genérica excluidos del conteo de CBO (ver justificación arriba).
# Nota: 'sqlite3', 'pymysql', etc. NO se excluyen - representan acoplamiento real.
EXCLUDED_MODULES = {"os", "sys"}


class ImportCollector(ast.NodeVisitor):
    """Primera pasada: recolecta qué módulos y símbolos se importan."""

    def __init__(self):
        self.imported_modules = set()
        self.imported_symbols = set()

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name.split(".")[0]
            self.imported_modules.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.imported_symbols.add(name)
        self.generic_visit(node)


class CBOVisitor(ast.NodeVisitor):
    """Segunda pasada: recorre cada clase y detecta uso de símbolos importados,
    excluyendo módulos de utilidad genérica (EXCLUDED_MODULES)."""

    def __init__(self, imported_modules, imported_symbols):
        self.imported_modules = imported_modules - EXCLUDED_MODULES
        self.imported_symbols = imported_symbols
        self.class_couplings = {}
        self.current_class = None

    def visit_ClassDef(self, node):
        previous_class = self.current_class
        self.current_class = node.name
        self.class_couplings.setdefault(node.name, set())

        for base in node.bases:
            base_name = self._root_name(base)
            if base_name and base_name != node.name:
                self.class_couplings[node.name].add(self._describe(base))

        self.generic_visit(node)
        self.current_class = previous_class

    def visit_Attribute(self, node):
        if self.current_class:
            root = self._root_name(node)
            if root in self.imported_modules:
                self.class_couplings[self.current_class].add(self._describe(node))
        if isinstance(node.value, (ast.Attribute, ast.Name)):
            return
        self.generic_visit(node)

    def visit_Name(self, node):
        if self.current_class and node.id in self.imported_symbols:
            self.class_couplings[self.current_class].add(node.id)
        self.generic_visit(node)

    def _root_name(self, node):
        while isinstance(node, ast.Attribute):
            node = node.value
        if isinstance(node, ast.Name):
            return node.id
        return None

    def _describe(self, node):
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
        return ".".join(reversed(parts))


def calculate_cbo(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=filepath)

    import_collector = ImportCollector()
    import_collector.visit(tree)

    cbo_visitor = CBOVisitor(import_collector.imported_modules, import_collector.imported_symbols)
    cbo_visitor.visit(tree)

    results = {}
    for class_name, coupled in cbo_visitor.class_couplings.items():
        results[class_name] = {
            "cbo": len(coupled),
            "coupled_to": sorted(coupled),
        }
    return results


if __name__ == "__main__":
    if len(sys_module.argv) < 2:
        print("Uso: python cbo_calculator.py <ruta_del_archivo.py>")
        sys_module.exit(1)

    filepath = sys_module.argv[1]
    results = calculate_cbo(filepath)

    print(f"\nResultados de CBO para: {filepath}\n")
    for class_name, data in results.items():
        print(f"  Clase: {class_name}")
        print(f"    CBO: {data['cbo']}")
        print(f"    Acoplada a: {data['coupled_to']}")
        print()
