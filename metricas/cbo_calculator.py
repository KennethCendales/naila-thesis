"""
NAILA - Calculador de CBO (Coupling Between Objects) - v2
Implementa la definición de Chidamber & Kemerer (1994): CBO(c) = número de
clases externas distintas a las que la clase c está acoplada.

v2 (Día 22, ampliado): en vez de detectar acoplamiento solo en llamadas y
anotaciones de tipo, se rastrean los imports del archivo y se detecta el uso
de esos símbolos importados en CUALQUIER contexto dentro de la clase
(llamadas, anotaciones, diccionarios, listas, valores por defecto, etc.).
Esto corrige la subestimación detectada en la v1, que no capturaba
referencias a clases externas usadas como valores literales (ej.
pymysql.cursors.DictCursor dentro de un diccionario de configuración).

Limitación conocida y documentada: no distingue entre acoplamiento a CLASES
específicamente vs. acoplamiento a funciones o constantes del mismo módulo
importado - se aproxima contando cualquier símbolo importado referenciado,
siguiendo un criterio conservador pero consistente entre todos los archivos
medidos (NAILA y ad hoc, ambos casos de estudio).

Uso: python cbo_calculator.py <ruta_del_archivo.py>
"""

import ast
import sys


class ImportCollector(ast.NodeVisitor):
    """Primera pasada: recolecta qué módulos y símbolos se importan."""

    def __init__(self):
        self.imported_modules = set()   # ej: 'pymysql' de 'import pymysql'
        self.imported_symbols = set()   # ej: 'OsCommerceACL' de 'from x import OsCommerceACL'

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
    """Segunda pasada: recorre cada clase y detecta uso de símbolos importados."""

    def __init__(self, imported_modules, imported_symbols):
        self.imported_modules = imported_modules
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
        # Evita doble conteo: si node.value es a su vez un Attribute o Name,
        # ya fue completamente capturado por _describe()/_root_name() al
        # recorrer la cadena hacia la raíz - no hace falta re-visitarlo.
        # Solo se continúa el recorrido si node.value es algo más complejo
        # (ej. una llamada a función), donde SÍ podrían existir otros
        # acoplamientos independientes por descubrir.
        if isinstance(node.value, (ast.Attribute, ast.Name)):
            return
        self.generic_visit(node)

    def visit_Name(self, node):
        if self.current_class and node.id in self.imported_symbols:
            self.class_couplings[self.current_class].add(node.id)
        self.generic_visit(node)

    def _root_name(self, node):
        """Devuelve el identificador raíz de una cadena de atributos, ej. pymysql.cursors.DictCursor -> 'pymysql'."""
        while isinstance(node, ast.Attribute):
            node = node.value
        if isinstance(node, ast.Name):
            return node.id
        return None

    def _describe(self, node):
        """Devuelve una representación legible de la cadena completa, ej. 'pymysql.cursors.DictCursor'."""
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
    if len(sys.argv) < 2:
        print("Uso: python cbo_calculator.py <ruta_del_archivo.py>")
        sys.exit(1)

    filepath = sys.argv[1]
    results = calculate_cbo(filepath)

    print(f"\nResultados de CBO para: {filepath}\n")
    for class_name, data in results.items():
        print(f"  Clase: {class_name}")
        print(f"    CBO: {data['cbo']}")
        print(f"    Acoplada a: {data['coupled_to']}")
        print()
