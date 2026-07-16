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
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

# Mismos valores categóricos vistos en tickets.parquet durante el entrenamiento.
CanalTicket = Literal["Whatsapp", "Correo", "Página Web"]
CategoriaProblema = Literal["Cuenta", "Fraude", "Técnica", "Cobros", "Pregunta general", "Otro"]
UsuarioTipoCuenta = Literal["Free", "Premium", "Business"]
NivelPrioridad = Literal["Baja", "Media", "Alta", "Critica"]


class PredictionRequest(BaseModel):
    """Payload de entrada para /predict."""

    model_config = ConfigDict(strict=True)

    # Atributos del ticket
    asunto_ticket: str = Field(..., min_length=1, description="Asunto del ticket.")
    contenido_ticket: str = Field(..., min_length=1, description="Descripción/cuerpo del ticket.")
    canal_ticket: CanalTicket = Field(..., description="Canal por el que llegó el ticket.")
    categoria_problema: CategoriaProblema = Field(..., description="Categoría del problema reportado.")

    # Atributos del usuario
    usuario_tipo_cuenta: UsuarioTipoCuenta = Field(..., description="Tipo de cuenta del usuario.")
    usuario_antiguedad_dias: int = Field(..., ge=0, description="Antigüedad de la cuenta del usuario, en días.")


class PredictionResponse(BaseModel):
    """Respuesta de /predict."""

    model_config = ConfigDict(strict=True)

    nivel_prioridad: NivelPrioridad = Field(..., description="Nivel de prioridad predicho para el ticket.")
