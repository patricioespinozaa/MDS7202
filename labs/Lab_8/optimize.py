import os
import pickle
from datetime import datetime

import mlflow
import mlflow.sklearn
import optuna
import pandas as pd
import sklearn
import xgboost
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

"""
Considerando el objetivo planteado, se le pide completar la función `optimize_model`, la cual debe:
- **Optimizar los hiperparámetros del modelo `XGBoost` usando `Optuna`.** Realice una cantidad de iteraciones para evitar tiempos de ejecución excesivos (al menos 10) check
- **Registrar cada entrenamiento en un experimento nuevo**, asegurándose de que la métrica `f1-score` se registre como `"valid_f1"`. No se deben guardar todos los experimentos en *Default*; en su lugar, cada `experiment` y `run` deben tener nombres interpretables, reconocibles y diferentes a los nombres por defecto (por ejemplo, para un run: "XGBoost con lr 0.1").
- **Devolver el mejor modelo** usando la función `get_best_model` y serializarlo en el disco con `pickle.dump`. Luego, guardar el modelo en la carpeta `/models`.
- **Guardar el código en `optimize.py`**. La ejecución de `python optimize.py` debería ejecutar la función `optimize_model`.
- **Guardar las versiones de las librerías utilizadas** en el desarrollo.

*Hint: Le puede ser útil revisar los parámetros que recibe `mlflow.start_run`*

```python
def get_best_model(experiment_id):
    runs = mlflow.search_runs(experiment_id)
    best_model_id = runs.sort_values("metrics.valid_f1")["run_id"].iloc[0]
    best_model = mlflow.sklearn.load_model("runs:/" + best_model_id + "/model")

    return best_model
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_best_model(experiment_id):
    runs = mlflow.search_runs(experiment_id)
    best_model_id = runs.sort_values("metrics.valid_f1")["run_id"].iloc[0]
    best_model = mlflow.sklearn.load_model("runs:/" + best_model_id + "/model")

    return best_model


def objective(trial):
    df = pd.read_csv(os.path.join(BASE_DIR, "water_potability.csv"))
    X = df.drop("Potability", axis=1)
    y = df["Potability"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "random_state": 42,
        "eval_metric": "logloss",
    }

    run_name = (
        f"XGBoost lr={params['learning_rate']:.3f} depth={params['max_depth']}"  # nombre distintivo para cada run
    )

    with mlflow.start_run(run_name=run_name):
        model = XGBClassifier(**params)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        f1 = f1_score(y_test, preds)

        mlflow.log_params(params)
        mlflow.log_metric("valid_f1", f1)  # loggear el f1-score con el nombre "valid_f1"
        mlflow.sklearn.log_model(model, artifact_path="model")

    return f1


def optimize_model():
    mlflow.set_tracking_uri(f"file://{os.path.join(BASE_DIR, 'mlruns')}")
    date_str = datetime.now()  # nombre del modelo con la fecha actual

    experiment_name = f"Optuna_XGBoost_Water_Potability_{date_str}"  # nombre del experimento con la fecha actual
    mlflow.set_experiment(
        experiment_name
    )  # creamos un nuevo experimento para cada entrenamiento, con un nombre distintivo
    experiment = mlflow.get_experiment_by_name(experiment_name)

    study = optuna.create_study(
        study_name="xgboost_optimization", direction="maximize"
    )  # Usar optuna para maximizar el f1-score
    study.optimize(objective, n_trials=10)  # usamos solo 10 iteraciones para evitar tiempos de ejecución excesivos

    print(f"Mejor f1-score: {study.best_value:.4f}")
    print(f"Mejores parámetros: {study.best_params}")

    best_model = get_best_model(
        experiment.experiment_id
    )  # devolvemos el mejor experimento usando la función get_best_model

    models_dir = os.path.join(BASE_DIR, "models")  # creamos la carpeta models si no existe
    os.makedirs(models_dir, exist_ok=True)

    with open(os.path.join(models_dir, f"xgb_{date_str}.pkl"), "wb") as f:
        pickle.dump(best_model, f)

    versions = {  # guardamos las versiones de las librerías utilizadas
        "mlflow": mlflow.__version__,
        "optuna": optuna.__version__,
        "sklearn": sklearn.__version__,
        "xgboost": xgboost.__version__,
    }

    with open(os.path.join(models_dir, f"library_versions_{date_str}.pkl"), "wb") as f:
        pickle.dump(versions, f)  # searilizar con pickle dump

    print(f"Modelo guardado en {models_dir}/xgb_{date_str}.pkl")  # guardamos en models
    print(f"Versiones guardadas: {versions}")

    return best_model


if __name__ == "__main__":  # ejecutar la función optimize_model al correr el script
    optimize_model()
