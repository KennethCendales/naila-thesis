"""
NAILA - Prueba end-to-end de la version AD HOC (baseline) - osCommerce
Mismo flujo conceptual que la version NAILA, pero llamando funciones sueltas
en vez de Adapter/ACL separados.

Instrumentado con medición de latencia en dos niveles (Día 23).

Ejecutar: python test_flujo_adhoc.py
"""

import json
import sys
import os
import requests

import integracion_adhoc as adhoc

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "metricas"))
from timing_utils import now, ms_between, registrar_medicion

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3.5:9b"


def preguntar_al_agente(mensaje_usuario):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": mensaje_usuario}],
        "tools": adhoc.TOOL_DEFINITIONS,
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()


def procesar_mensaje(mensaje_usuario):
    print(f"\nUsuario: {mensaje_usuario}")

    t0 = now()
    respuesta = preguntar_al_agente(mensaje_usuario)
    mensaje_modelo = respuesta.get("message", {})

    tool_calls = mensaje_modelo.get("tool_calls", [])
    if not tool_calls:
        print("El modelo no solicitó ninguna herramienta. Respuesta directa:")
        print(mensaje_modelo.get("content"))
        return

    for call in tool_calls:
        function_name = call["function"]["name"]
        arguments = call["function"].get("arguments", {})
        print(f"[Agente solicita] {function_name}({arguments})")

        funcion = getattr(adhoc, function_name, None)
        if funcion is None:
            print(f"Función no reconocida: {function_name}")
            continue

        t1 = now()
        resultado = funcion(**arguments)
        t2 = now()

        nivel1_ms = ms_between(t1, t2)
        nivel2_ms = ms_between(t0, t2)

        print("[Función ad hoc devolvió]:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print(f"[Latencia] Nivel 1 (sin LLM): {nivel1_ms} ms")
        print(f"[Latencia] Nivel 2 (con LLM): {nivel2_ms} ms")

        registrar_medicion("oscommerce", "adhoc", function_name, nivel1_ms, nivel2_ms)


def main():
    casos_de_prueba = [
        "muéstrame los productos disponibles",
        "busca productos que tengan Weapon en el nombre",
        "¿cuál es el estado del pedido número 1?",
    ]
    for mensaje in casos_de_prueba:
        procesar_mensaje(mensaje)


if __name__ == "__main__":
    main()
