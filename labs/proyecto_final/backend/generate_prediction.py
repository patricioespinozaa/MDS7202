"""
Construya una función que dados los mínimos campos necesarios construya el input del pipeline entrenado anteriormente y luego utilice el pipeline para obtener la categoría.
- Guarde el pipeline completo en un archivo .pickle
- Cree la función ``generate_prediction`` que tome la menor cantidad de parámetros necesarios requeridos y retorne la predicción. Esta función deberá:
  - Vectorizar el texto de forma idéntica a como se construyeron los embeddings que le fueron dados. Para esto:
    - Concatene el asunto y descripción de esta forma: `Asunto_Ticket: {asunto}\nContenido_Ticket: {contenido}\n`
    - Utilice la clase `GoogleGenerativeAIEmbeddings` de langchain con el modelo `gemini-embedding-001` y la opción `output_dimensionality=1024` para vectorizar el texto de forma análoga a lo que le fue entregado.
  - Procesar el resto de features hasta obtener las mismas variables que usó para la construcción del modelo
  - Cargar el pipeline desde el .pickle y utilizarlo para generar una predicción en base a estas variables
  - Retornar la predicción
- Guarde todo este código en un archivo ``backend/generate_prediction.py``
- Incluya una sección al final de este script que ejecute la función con datos de muestra cuando el script se ejecuta directamente (no a través de una importación)

Finalmente, incluya un screenshot o un link a un screenshot con el output

**⚠️Cuidado: para que funcione deberá incluir su GOOGLE_API_KEY en un archivo de configuración como un .env. RECUERDE NO AGREGAR ESE ARCHIVO AL REPOSITORIO**

**⚠️Se revisará que su código refleje 100% el modelo entrenado. Si es necesario, explore los datos para deducir como algunos atributos fueron construidos (como N_Caracteres_Ticket)**
"""

import os
from pathlib import Path

import cloudpickle
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

EMBEDDING_MODEL = "models/gemini-embedding-001"
EMBEDDING_DIMENSION = 1024
MODEL_PATH = Path(__file__).resolve().parent / "modelo_final.pkl"

try:
    os.environ["GOOGLE_API_KEY"]
except KeyError as err:
    raise KeyError("La variable de entorno GOOGLE_API_KEY no está definida. ") from err

# Carga del pipeline entrenado desde el archivo .pickle
# Utilizamos el formato .pkl en vez de .pickle ya que al buscar en internet salen como equivalentes y por otra parte el .pkl
# es el formato que venia definido en la Parte 2

# Aunque en la parte 2 justificamos el por qué a nuestro juicio RL + Embeddings es mejor que MLP + Embeddings,
# en el .pkl se utiliza el pipeline de MLP + Embeddings, ya que es el que se descaga al obtener un test ligeramente más alto.
# ColumnTransformer solo selecciona las columnas embedding_dim_* (ver Parte 2), por lo que ninguna otra
# feature tabular (N_Caracteres_Ticket, Canal_Ticket, Categoría_Problema, Texto) es necesaria en este script.
try:
    with open(MODEL_PATH, "rb") as f:
        _pipeline = cloudpickle.load(f)
except FileNotFoundError as err:
    raise FileNotFoundError(f"No se encontró el archivo {MODEL_PATH}. ") from err


try:
    _embeddings_client = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        output_dimensionality=EMBEDDING_DIMENSION,
        google_api_key=os.environ["GOOGLE_API_KEY"],
    )
except Exception as e:
    raise RuntimeError("No se pudo inicializar el cliente de embeddings. ") from e


def generate_prediction(asunto_ticket: str, contenido_ticket: str) -> str:
    """Predice el Nivel_Prioridad de un ticket.

    El pipeline final (MLP + Embeddings) solo consume los embeddings del texto,
    por lo que estos dos campos son los únicos necesarios para generar la predicción.

    Args:
        asunto_ticket: Asunto del ticket.
        contenido_ticket: Descripción del ticket.

    Returns:
        El Nivel_Prioridad predicho: "Baja", "Media", "Alta" o "Critica".
    """
    # Vectorización siguiendo el mismo formato usado para generar los embeddings de entrenamiento.
    texto_embedding = f"Asunto_Ticket: {asunto_ticket}\nContenido_Ticket: {contenido_ticket}\n"
    vector = _embeddings_client.embed_query(texto_embedding)

    fila = {f"embedding_dim_{i}": valor for i, valor in enumerate(vector, start=1)}

    X = pd.DataFrame([fila])
    prediccion = _pipeline.predict(X)[0]
    return prediccion


if __name__ == "__main__":
    resultado = generate_prediction(
        asunto_ticket="Transferencia fallida y dinero descontado",
        contenido_ticket=(
            "Hola, intenté hacer una transferencia a otro banco y me descontaron la plata "
            "pero el destinatario dice que nunca le llegó. Necesito que revisen esto urgente "
            "porque es un monto importante."
        ),
    )
    print("Predicción de Nivel_Prioridad:", resultado)
