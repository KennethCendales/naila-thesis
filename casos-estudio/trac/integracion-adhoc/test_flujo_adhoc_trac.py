"""
NAILA - Prueba end-to-end de la version AD HOC (baseline) - Trac
Mismo flujo conceptual que la version NAILA, pero llamando funciones sueltas
en vez de Adapter/ACL separados.

Ejecutar: python test_flujo_adhoc_trac.py
"""

import json
import requests

import integracion_adhoc_trac as adhoc

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

        resultado = funcion(**arguments)
        print("[Función ad hoc devolvió]:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))


def main():
    casos_de_prueba = [
        "muéstrame los tickets que están abiertos",
        "busca tickets relacionados con login",
        "dame los detalles completos del ticket número 1",
    ]
    for mensaje in casos_de_prueba:
        procesar_mensaje(mensaje)


if __name__ == "__main__":
    main()
