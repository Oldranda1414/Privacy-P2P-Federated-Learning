FROM python:3.10-slim

WORKDIR /app

# Install python build manager
RUN pip install uv

# Install deps (for caching)
COPY src/pyproject.toml src/uv.lock ./src/
RUN uv sync --frozen --project src

COPY src/ ./src

ENTRYPOINT ["uv", "--project", "src", "run", "src/main/main.py"]
