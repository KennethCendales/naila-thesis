"""
NAILA - Demo de chat web funcional (backend) - v2
Agrega: endpoint de catálogo real (/products) y enriquecimiento de resultados
de productos con el link real a la página de osCommerce, para que el usuario
pueda navegar directamente al producto.

IMPORTANTE: sigue reutilizando (sin modificar) el código de producción ya
medido empíricamente (casos-estudio/oscommerce/integracion-naila/).
El enriquecimiento con "url" ocurre aquí, en la capa de demo, no en el ACL/Adapter medido.

Ejecutar:
    uvicorn app:app --reload --port 8000
"""

import sys
import os
import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "casos-estudio", "oscommerce", "integracion-naila"
))
from oscommerce_adapter import OsCommerceAdapter, TOOL_DEFINITIONS

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3.5:9b"
STORE_BASE_URL = "http://localhost:8080"

app = FastAPI(title="NAILA Chat Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

adapter = OsCommerceAdapter()


class ChatRequest(BaseModel):
    message: str


def obtener_mapa_nombres(limit=100):
    """
    Construye un mapa {id: nombre_real} usando search_products_by_name con
    keyword vacío (coincide con todos los nombres vía LIKE '%%'), ya que
    list_available_products no incluye el campo 'name' (solo 'model').
    No modifica el Adapter medido - solo lo reutiliza con otro propósito.
    """
    resultado = adapter.search_products_by_name(keyword="", limit=limit)
    return {p["id"]: p["name"] for p in resultado["products"]}


def enriquecer_con_url(resultado):
    """
    Agrega el link real al producto (product_info.php?products_id=N) y,
    si falta, el nombre real del producto (en vez del código de modelo/SKU),
    a cada producto de un resultado del Adapter.
    """
    if isinstance(resultado, dict) and "products" in resultado:
        nombres = None
        for producto in resultado["products"]:
            producto["url"] = f"{STORE_BASE_URL}/product_info.php?products_id={producto['id']}"
            if "name" not in producto:
                if nombres is None:
                    nombres = obtener_mapa_nombres()
                producto["name"] = nombres.get(producto["id"], producto.get("model"))
    return resultado


def llamar_ollama(messages, incluir_tools=True):
    payload = {"model": MODEL_NAME, "messages": messages, "stream": False}
    if incluir_tools:
        payload["tools"] = TOOL_DEFINITIONS
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()


@app.post("/chat")
def chat(request: ChatRequest):
    messages = [
        {
            "role": "system",
            "content": (
                "Eres el asistente virtual de Pola Store. Reglas estrictas de formato:\n"
                "1. Responde SIEMPRE de forma breve y directa, sin saludos largos ni relleno.\n"
                "2. Cuando listes productos, usa una lista con viñetas (una línea por producto), NUNCA tablas.\n"
                "3. NUNCA muestres una URL visible como texto plano. Oculta siempre el link "
                "detrás del NOMBRE REAL del producto (campo 'name'), usando formato Markdown: "
                "[nombre](url). NUNCA uses el campo 'model' (es un código SKU interno, no un nombre "
                "presentable al usuario).\n"
                "4. No inventes información que no provenga de las herramientas.\n\n"
                "Ejemplo exacto del formato esperado para listar productos:\n"
                "En Pola Store tenemos 3 productos:\n"
                "- [Matrox G200 MMS](http://localhost:8080/product_info.php?products_id=1)\n"
                "- [Lethal Weapon](http://localhost:8080/product_info.php?products_id=13)\n"
                "- [The Matrix](http://localhost:8080/product_info.php?products_id=6)\n\n"
                "Sigue exactamente ese estilo: sin tabla, sin URL visible, nombre real (no código "
                "de modelo), una viñeta por producto sin excepción."
            ),
        },
        {"role": "user", "content": request.message},
    ]

    respuesta = llamar_ollama(messages)
    mensaje_modelo = respuesta.get("message", {})
    tool_calls = mensaje_modelo.get("tool_calls", [])

    if not tool_calls:
        return {"reply": mensaje_modelo.get("content", "")}

    messages.append(mensaje_modelo)
    for call in tool_calls:
        function_name = call["function"]["name"]
        arguments = call["function"].get("arguments", {})
        metodo = getattr(adapter, function_name, None)

        if metodo is None:
            resultado = {"error": f"Herramienta no reconocida: {function_name}"}
        else:
            resultado = metodo(**arguments)
            resultado = enriquecer_con_url(resultado)

        messages.append({"role": "tool", "content": json.dumps(resultado, ensure_ascii=False)})

    respuesta_final = llamar_ollama(messages, incluir_tools=False)
    return {"reply": respuesta_final.get("message", {}).get("content", "")}


@app.get("/products")
def get_products(limit: int = 8):
    """
    Catálogo real para mostrar en la tienda simulada.
    Reutiliza search_products_by_name con keyword vacío (coincide con todos
    los nombres vía LIKE '%%'), sin modificar el Adapter medido.
    """
    resultado = adapter.search_products_by_name(keyword="", limit=limit)
    resultado = enriquecer_con_url(resultado)
    return resultado


@app.get("/health")
def health():
    return {"status": "ok"}
