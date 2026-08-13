"""
NAILA - Prueba end-to-end: primer caso de uso funcional
Usuario (lenguaje natural) -> Agente LLM (Qwen3.5-9B vía Ollama) -> Adapter -> ACL -> osCommerce

Ejecutar: python test_flujo_completo.py
"""

import json
import requests

from oscommerce_adapter import OsCommerceAdapter, TOOL_DEFINITION

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3.5:9b"


def preguntar_al_agente(mensaje_usuario):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": mensaje_usuario}],
        "tools": [TOOL_DEFINITION],
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()


def main():
    mensaje_usuario = "muéstrame los productos disponibles"
    print(f"Usuario: {mensaje_usuario}\n")

    respuesta = preguntar_al_agente(mensaje_usuario)
    mensaje_modelo = respuesta.get("message", {})

    tool_calls = mensaje_modelo.get("tool_calls", [])
    if not tool_calls:
        print("El modelo no solicitó ninguna herramienta. Respuesta directa:")
        print(mensaje_modelo.get("content"))
        return

    adapter = OsCommerceAdapter()

    for call in tool_calls:
        function_name = call["function"]["name"]
        arguments = call["function"].get("arguments", {})
        print(f"[Agente solicita] {function_name}({arguments})")

        if function_name == "list_available_products":
            resultado = adapter.list_available_products(**arguments)
            print("\n[Adapter -> ACL -> osCommerce devolvió]:")
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        else:
            print(f"Función no reconocida: {function_name}")


if __name__ == "__main__":
    main()
