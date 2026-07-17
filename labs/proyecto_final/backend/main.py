"""
Construya la app de FastApi que habilite un endpoint para realizar la predicción.

- Cree el archivo `backend/main.py` donde definirá sus endpoints. Importe la función `generate_prediction`
- Cree el archivo `backend/models.py`. Defina en él los modelos de `pydantic` para la request (`PredictionRequest`)
  y response (`PredictionResponse`). Su endpoint debe tener tipado **estricto** y arrojar error 422 (gestionado por fastapi)
  cuando los argumentos de la request no cumplan con el tipo esperado.
- Cree un endpoint de tipo **POST** con la ruta `/predict` que reciba un payload del tipo `PredictionRequest` y que llame a
  la función `generate_prediction`, retornando la predicción en un objeto `PredictionResponse`.
- Agregue clausulas de `try/except` que envuelvan la llamada a `generate_prediction` y lance una `HttpException` en caso de error.
- Levante su app de fastapi usando `uvicorn`
- Llame a su app de fastapi usando postman o requests. Incluya una screenshot del input y output de una llamada exitosa, y el input y output de una llamada no exitosa.
"""

from fastapi import FastAPI, HTTPException
from generate_prediction import generate_prediction
from models import PredictionRequest, PredictionResponse

app = FastAPI(title="ChaucherApp - Priorización de Tickets")


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Endpoint para predecir el nivel de prioridad de un ticket.
    Args:
        request (PredictionRequest): Payload de entrada con los datos del ticket.
    Returns:
        PredictionResponse: Respuesta con el nivel de prioridad predicho.
    """
    try:
        nivel_prioridad = generate_prediction(
            asunto_ticket=request.asunto_ticket,
            contenido_ticket=request.contenido_ticket,
            canal_ticket=request.canal_ticket,
            categoria_problema=request.categoria_problema,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al generar la predicción: {exc}") from exc

    return PredictionResponse(nivel_prioridad=nivel_prioridad)
