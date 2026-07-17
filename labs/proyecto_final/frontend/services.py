import os

import requests
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.environ["BACKEND_URL"]


def enviar_prediccion(asunto_ticket: str, contenido_ticket: str) -> str:
    """Llama al endpoint /predict del backend y retorna el Nivel_Prioridad predicho.

    Si la llamada falla (error de red o respuesta con error), retorna un mensaje
    de error legible en vez de lanzar una excepción.

    Args:
        asunto_ticket: Asunto del ticket.
        contenido_ticket: Contenido del ticket.
    Returns:
        El Nivel_Prioridad predicho: "Baja", "Media", "Alta", "Critica" o un mensaje de error legible.
    """
    payload = {
        "asunto_ticket": asunto_ticket,
        "contenido_ticket": contenido_ticket,
    }

    try:
        response = requests.post(f"{BACKEND_URL}/predict", json=payload, timeout=30)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        detalle = response.json().get("detail", response.text)
        return f"Error del servidor ({response.status_code}): {detalle}"
    except requests.exceptions.RequestException as exc:
        return f"No se pudo contactar al backend: {exc}"

    return response.json()["nivel_prioridad"]
