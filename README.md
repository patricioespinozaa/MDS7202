# MDS7202 - Laboratorio de Programación Científica para Ciencia de Datos

Repositorio del curso MDS7202 (Otoño 2026), Facultad de Ciencias Físicas y Matemáticas, Universidad de Chile.

Este repositorio contiene los laboratorios y entregas del curso, organizados por carpetas según cada laboratorio.

## Integrantes

| Nombre | GitHub |
|--------|--------|
| Javiera Romero | [@javiromeroo](https://github.com/javiromeroo) |
| Patricio Espinoza | [@patricioespinozaa](https://github.com/patricioespinozaa) |

## Estructura del repositorio

```
.
├── labs/
│   ├── lab_1/             Python y Git
│   ├── lab_2/             Imágenes
│   ├── lab_3/             El Pandas no muerde (act. I)
│   ├── lab_4/             EDA en Pandas
│   ├── lab_5/             La desesperación de Mr. Lepin
│   ├── lab_6/             ¿A cuánto la casa?
│   ├── lab_7/             Ensamblaje, Optimización de Hiperparámetros e Interpretabilidad
│   ├── lab_8/             Ready, Set, Deploy!
│   ├── lab_9/             Benchmark de Carga y Modelos con Spotify
│   ├── lab_10/           Chatbot 101
│   └── proyecto_final/    Proyecto final: priorización de tickets de soporte (ChaucherApp)
│       ├── Enunciado_Parte1_Analisis.ipynb    Análisis exploratorio de datos y embeddings
│       ├── Enunciado_Parte2_Modelo.ipynb      Experimentación de modelos (Optuna + MLflow)
│       ├── Enunciado_Parte3_Despliegue.ipynb  Despliegue del modelo
│       ├── backend/                           API (FastAPI) que sirve el modelo entrenado
│       └── frontend/                          Interfaz para consumir la API
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md
```

## Configuración del entorno

```bash
uv venv
source .venv/bin/activate
uv sync
pre-commit install
```

### Proyecto final

Para correr el proyecto final (`labs/proyecto_final/`) es necesario:

- Un archivo `.env` con una `GOOGLE_API_KEY` para generar embeddings con `gemini-embedding-001` tanto en el notebook de la Parte 1 como en el backend de la Parte 3.
- MLflow como backend de tracking local (usado en la Parte 2):

  ```bash
  cd labs/proyecto_final
  mlflow ui --backend-store-uri sqlite:///mlflow.db
  ```

- Para levantar el backend y frontend con Docker:

  ```bash
  cd labs/proyecto_final
  docker compose up --build
  ```
