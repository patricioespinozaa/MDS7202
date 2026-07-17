FROM python:3.12-slim

# uv, copiado desde su imagen oficial (patrón recomendado por astral-sh).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN uv sync --frozen

EXPOSE 7860

CMD ["uv", "run", "python", "app.py"]
