"""
Con el modelo ya entrenado, la idea de esta sección es generar una API REST a la cual se le pueda hacer *requests* para así interactuar con su modelo. En particular, se le pide:

- Guardar el código de esta sección en el archivo `main.py`. Note que ejecutar `python main.py` debería levantar el servidor en el puerto por defecto.
- Defina `GET` con ruta tipo *home* que describa brevemente su modelo, el problema que intenta resolver, su entrada y salida.
- Defina un `POST` a la ruta `/potabilidad/` donde utilice su mejor optimizado para predecir si una medición de agua es o no potable. Por ejemplo, una llamada de esta ruta con un *body*:

```json
{
   "ph":10.316400384553162,
   "Hardness":217.2668424334475,
   "Solids":10676.508475429378,
   "Chloramines":3.445514571005745,
   "Sulfate":397.7549459751925,
   "Conductivity":492.20647361771086,
   "Organic_carbon":12.812732207582542,
   "Trihalomethanes":72.28192021570328,
   "Turbidity":3.4073494284238364
}
```

Su servidor debería retornar una respuesta HTML con código 200 con:


```json
{
  "potabilidad": 0 # respuesta puede variar según el clasificador que entrenen
}
```

**`HINT:` Recuerde que puede utilizar [http://localhost:8000/docs](http://localhost:8000/docs) para hacer un `POST`.**
"""

import pickle

import uvicorn
from fastapi import FastAPI

# crear aplicación
app = FastAPI()
# cargar el mejor modelo obtenido en la sección anterior con pickle.load

with open("models/xgb_2026-06-10 13:09:33.908341.pkl", "rb") as f:
    best_model = pickle.load(f)


# def home
@app.get("/")
def home():
    """{
      "descripcion": "Modelo de clasificación binaria XGBoost optimizado con Optuna para predecir la potabilidad del agua",
      "problema": "Se desea resolver el problema de predecir si una muestra de agua es potable (1) o no potable (0)",
      "entrada": {
        "ph": "float",
        "Hardness": "float",
        "Solids": "float",
        "Chloramines": "float",
        "Sulfate": "float",
        "Conductivity": "float",
        "Organic_carbon": "float",
        "Trihalomethanes": "float",
        "Turbidity": "float"
      },
      "salida": {
        "potabilidad": "0 (no potable) o 1 (potable)"
      }
    }"""
    return {
        "descripcion": "Modelo de clasificación binaria XGBoost optimizado con Optuna para predecir la potabilidad del agua",
        "problema": "Se desea resolver el problema de predecir si una muestra de agua es potable (1) o no potable (0)",
        "entrada": {
            "ph": "float",
            "Hardness": "float",
            "Solids": "float",
            "Chloramines": "float",
            "Sulfate": "float",
            "Conductivity": "float",
            "Organic_carbon": "float",
            "Trihalomethanes": "float",
            "Turbidity": "float",
        },
        "salida": {"potabilidad": "0 (no potable) o 1 (potable)"},
    }


@app.post("/potabilidad/")  # ruta
def predict(
    ph: float,
    Hardness: float,
    Solids: float,
    Chloramines: float,
    Sulfate: float,
    Conductivity: float,
    Organic_carbon: float,
    Trihalomethanes: float,
    Turbidity: float,
) -> dict[str, str]:  # parametros de entrada
    label = best_model.predict(
        [[ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]]
    )[0]  # generar prediccion con mejor modelo obtenido en la seccion anterior
    return {"potabilidad": str(label)}  # retornar prediccion


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
