"""
NAILA - Utilidades de medición de latencia (Día 23, Fase 4)

Define dos niveles de medición, coherentes con operacionalizacion-variables.md:
- Nivel 1 (capa de integración): tiempo desde que el agente ya decidió qué
  herramienta usar (post-inferencia) hasta que el Adapter/ACL devuelve el
  resultado traducido. EXCLUYE el tiempo de inferencia del LLM.
- Nivel 2 (sistema completo): tiempo end-to-end, desde que se envía el
  mensaje del usuario hasta que se obtiene el resultado final. INCLUYE la
  inferencia del LLM.

Los resultados se acumulan en metricas/resultados_latencia.csv para su
análisis conjunto en fases posteriores.
"""

import csv
import os
import time

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados_latencia.csv")
CSV_HEADERS = ["timestamp", "sistema", "version", "caso_de_uso", "nivel1_ms", "nivel2_ms"]


def now():
    """Marca de tiempo de alta resolución, en segundos (float)."""
    return time.perf_counter()


def ms_between(t_inicio, t_fin):
    """Convierte una diferencia de tiempo (segundos) a milisegundos."""
    return round((t_fin - t_inicio) * 1000, 3)


def registrar_medicion(sistema, version, caso_de_uso, nivel1_ms, nivel2_ms):
    """
    Agrega una fila de medición al CSV consolidado de resultados.
    sistema: 'oscommerce' o 'trac'
    version: 'naila' o 'adhoc'
    caso_de_uso: nombre de la función/tool invocada
    """
    archivo_existe = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(CSV_HEADERS)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            sistema,
            version,
            caso_de_uso,
            nivel1_ms,
            nivel2_ms,
        ])
