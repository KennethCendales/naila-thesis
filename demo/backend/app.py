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
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "casos-estudio", "oscommerce", "integracion-naila"
))
from oscommerce_adapter import OsCommerceAdapter, TOOL_DEFINITIONS
from oscommerce_acl import OsCommerceACL

# Configuración externalizada vía variables de entorno (para poder contenerizar
# el backend sin depender de "localhost", que dentro de un contenedor apunta
# al contenedor mismo, no al host). Los defaults preservan el comportamiento
# original para ejecución nativa (sin Docker).
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL_NAME = os.environ.get("MODEL_NAME", "qwen3.5:9b")
STORE_BASE_URL = os.environ.get("STORE_BASE_URL", "http://localhost:8080")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
OLLAMA_TIMEOUT = 40  # segundos

app = FastAPI(title="NAILA Chat Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

adapter = OsCommerceAdapter()
# Reasignación del ACL con el host configurable, SIN modificar oscommerce_adapter.py
# ni oscommerce_acl.py (archivos ya medidos empíricamente en las Fases 4-5).
# Esto es composición externa legítima: se sustituye el atributo público .acl
# después de construir el Adapter con su comportamiento original intacto.
adapter.acl = OsCommerceACL(host=MYSQL_HOST)

# --- Herramienta adicional (capa de demo, no forma parte de lo medido empíricamente) ---
# Permite responder preguntas frecuentes de la tienda con datos reales de un
# catálogo de políticas, en vez de dejar que el modelo improvise una respuesta.
POLITICAS_TIENDA = {
    "envios": "Pola Store realiza envíos nacionales en 3-5 días hábiles. Por el momento no se realizan envíos internacionales.",
    "devoluciones": "Aceptamos devoluciones dentro de los 15 días posteriores a la compra, con el producto en su empaque original.",
    "horario": "Atención al cliente: lunes a viernes, de 8:00 a.m. a 6:00 p.m.",
    "descuentos": "Los descuentos vigentes se muestran directamente en la página de cada producto. No manejamos descuentos por volumen actualmente.",
    "contacto": "Puedes escribir por este mismo chat o al correo soporte@polastore.demo.",
    "pago": "Aceptamos tarjetas de crédito/débito y pago contra entrega en ciudades principales.",
}

FAQ_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "consultar_politicas_tienda",
        "description": (
            "Consulta políticas generales de la tienda: envíos, devoluciones, "
            "horario de atención, descuentos, contacto o métodos de pago."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "tema": {
                    "type": "string",
                    "description": "Uno de: envios, devoluciones, horario, descuentos, contacto, pago",
                }
            },
            "required": ["tema"],
        },
    },
}


def consultar_politicas_tienda(tema):
    clave = (tema or "").lower().strip()
    respuesta = POLITICAS_TIENDA.get(clave)
    if respuesta is None:
        return {
            "encontrado": False,
            "mensaje": "No tengo información registrada sobre ese tema específico. "
            "Puedo ayudarte con envíos, devoluciones, horario, descuentos, contacto o pagos.",
        }
    return {"encontrado": True, "tema": clave, "respuesta": respuesta}


TODAS_LAS_HERRAMIENTAS = TOOL_DEFINITIONS + [FAQ_TOOL_DEFINITION]


class RespuestaAmigableError(Exception):
    """Error controlado: el mensaje ya es seguro y amigable para mostrar al usuario final."""
    def __init__(self, mensaje, status_code=503):
        self.mensaje = mensaje
        self.status_code = status_code


@app.exception_handler(RespuestaAmigableError)
async def manejar_error_amigable(request: Request, exc: RespuestaAmigableError):
    return JSONResponse(status_code=exc.status_code, content={"reply": exc.mensaje, "error": True})


@app.exception_handler(Exception)
async def manejar_error_inesperado(request: Request, exc: Exception):
    # Nunca exponer el traceback real al usuario final; queda igual visible en la consola de uvicorn.
    return JSONResponse(
        status_code=500,
        content={"reply": "Ocurrió un error inesperado en el servidor. Por favor intenta de nuevo.", "error": True},
    )


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
        payload["tools"] = TODAS_LAS_HERRAMIENTAS
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise RespuestaAmigableError(
            "El asistente no está disponible en este momento. Verifica que Ollama esté corriendo."
        )
    except requests.exceptions.Timeout:
        raise RespuestaAmigableError(
            "El asistente está tardando más de lo normal en responder. Intenta de nuevo en unos segundos."
        )
    except requests.exceptions.HTTPError as e:
        raise RespuestaAmigableError(
            f"El asistente respondió con un error inesperado ({e.response.status_code}). Intenta de nuevo."
        )


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
                "4. Para preguntas sobre envíos, devoluciones, horario, descuentos, contacto o pagos, "
                "usa SIEMPRE la herramienta consultar_politicas_tienda - nunca inventes esta información.\n"
                "5. Si una pregunta no puede responderse con ninguna herramienta disponible, dilo "
                "honestamente y de forma breve (ej. 'no tengo esa información disponible'). NUNCA "
                "inventes datos que no provengan de una herramienta.\n\n"
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

        if function_name == "consultar_politicas_tienda":
            resultado = consultar_politicas_tienda(**arguments)
        else:
            metodo = getattr(adapter, function_name, None)
            if metodo is None:
                resultado = {"error": f"Herramienta no reconocida: {function_name}"}
            else:
                try:
                    resultado = metodo(**arguments)
                    resultado = enriquecer_con_url(resultado)
                except Exception:
                    resultado = {
                        "error": "No se pudo consultar la tienda en este momento. "
                        "Verifica que osCommerce y su base de datos estén disponibles."
                    }

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
    try:
        resultado = adapter.search_products_by_name(keyword="", limit=limit)
        resultado = enriquecer_con_url(resultado)
        return resultado
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"count": 0, "products": [], "error": "No se pudo conectar con osCommerce."},
        )


@app.get("/health")
def health():
    return {"status": "ok"}
