FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN /usr/bin/uv sync --frozen --no-cache

# Run the application.
CMD ["uv","run",".venv/bin/fastapi", "run", "src/keyfort/main.py", "--port", "80", "--host", "0.0.0.0"]
