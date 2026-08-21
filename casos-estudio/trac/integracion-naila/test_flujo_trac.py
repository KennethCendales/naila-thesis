"""
NAILA - Prueba end-to-end sobre Trac (Días 18-19, instrumentado Día 23)
Usuario (lenguaje natural) -> Agente LLM (Qwen3.5-9B vía Ollama) -> Adapter -> ACL -> Trac

Ejecutar: python test_flujo_trac.py
"""

import json
import sys
import os
import requests

from trac_adapter import TracAdapter, TOOL_DEFINITIONS

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

        metodo = getattr(adapter, function_name, None)
        if metodo is None:
            print(f"Función no reconocida: {function_name}")
            continue

        t1 = now()
        resultado = metodo(**arguments)
        t2 = now()

        nivel1_ms = ms_between(t1, t2)
        nivel2_ms = ms_between(t0, t2)

        print("[Adapter -> ACL -> Trac devolvió]:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print(f"[Latencia] Nivel 1 (sin LLM): {nivel1_ms} ms")
        print(f"[Latencia] Nivel 2 (con LLM): {nivel2_ms} ms")

        registrar_medicion("trac", "naila", function_name, nivel1_ms, nivel2_ms)


def main():
    adapter = TracAdapter()
    casos_de_prueba = [
        "muéstrame los tickets que están abiertos",
        "busca tickets relacionados con login",
        "dame los detalles completos del ticket número 1",
    ]
    for mensaje in casos_de_prueba:
        procesar_mensaje(adapter, mensaje)


if __name__ == "__main__":
    main()
