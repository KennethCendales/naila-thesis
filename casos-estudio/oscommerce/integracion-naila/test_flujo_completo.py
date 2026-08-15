"""
NAILA - Prueba end-to-end: casos de uso de osCommerce (Día 16)
Usuario (lenguaje natural) -> Agente LLM (Qwen3.5-9B vía Ollama) -> Adapter -> ACL -> osCommerce

Ejecutar: python test_flujo_completo.py
"""

import json
import requests

from oscommerce_adapter import OsCommerceAdapter, TOOL_DEFINITIONS

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

        resultado = metodo(**arguments)
        print("[Adapter -> ACL -> osCommerce devolvió]:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))


def main():
    adapter = OsCommerceAdapter()

    casos_de_prueba = [
        "muéstrame los productos disponibles",
        "busca productos que tengan DVD en el nombre",
        "¿cuál es el estado del pedido número 1?",
    ]

    for mensaje in casos_de_prueba:
        procesar_mensaje(adapter, mensaje)


if __name__ == "__main__":
    main()
