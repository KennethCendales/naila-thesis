"""
NAILA - Prueba end-to-end: casos de uso de osCommerce (Día 16, instrumentado Día 23)
Usuario (lenguaje natural) -> Agente LLM (Qwen3.5-9B vía Ollama) -> Adapter -> ACL -> osCommerce

Instrumentado con medición de latencia en dos niveles (Día 23):
- Nivel 1: tiempo del Adapter/ACL, EXCLUYENDO la inferencia del LLM
- Nivel 2: tiempo end-to-end, INCLUYENDO la inferencia del LLM

Ejecutar: python test_flujo_completo.py
"""

import json
import sys
import os
import requests

from oscommerce_adapter import OsCommerceAdapter, TOOL_DEFINITIONS

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "metricas"))
from timing_utils import now, ms_between, registrar_medicion

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3.5:9b"


def preguntar_al_agente(mensaje_usuario):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": mensaje_usuario}],
        "tools": TOOL_DEFINITIONS,
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()


def procesar_mensaje(adapter, mensaje_usuario):
    print(f"\nUsuario: {mensaje_usuario}")

    t0 = now()  # Inicio Nivel 2 (incluye inferencia del LLM)
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

        metodo = getattr(adapter, function_name, None)
        if metodo is None:
            print(f"Función no reconocida: {function_name}")
            continue

        t1 = now()  # Inicio Nivel 1 (justo después de que el LLM ya decidió qué tool usar)
        resultado = metodo(**arguments)
        t2 = now()  # Fin Nivel 1 y fin Nivel 2 (no hay segunda llamada al LLM en este script)

        nivel1_ms = ms_between(t1, t2)
        nivel2_ms = ms_between(t0, t2)

        print("[Adapter -> ACL -> osCommerce devolvió]:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print(f"[Latencia] Nivel 1 (capa de integración, sin LLM): {nivel1_ms} ms")
        print(f"[Latencia] Nivel 2 (end-to-end, con LLM): {nivel2_ms} ms")

        registrar_medicion("oscommerce", "naila", function_name, nivel1_ms, nivel2_ms)


def main():
    adapter = OsCommerceAdapter()

    casos_de_prueba = [
        "muéstrame los primeros 10 productos disponibles",
        "busca productos que tengan Weapon en el nombre",
        "¿cuál es el estado del pedido número 1?",
    ]

    REPETICIONES = 10
    for i in range(REPETICIONES):
        print(f"\n{'='*50}\nRepetición {i+1}/{REPETICIONES}\n{'='*50}")
        for mensaje in casos_de_prueba:
            procesar_mensaje(adapter, mensaje)


if __name__ == "__main__":
    main()
