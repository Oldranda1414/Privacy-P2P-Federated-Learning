FROM python:3.10-slim

WORKDIR /app

# set environment variable for TensorFlow logging
ENV TF_CPP_MIN_LOG_LEVEL=3

# Install python build manager
RUN pip install uv

# Install deps (for caching)
COPY src/pyproject.toml src/uv.lock ./src/
RUN uv sync --frozen --project src

COPY dataset/ ./dataset
COPY src/ ./src
RUN rm -rf src/.venv

ENTRYPOINT ["uv", "--project", "src", "run", "src/main/main.py"]
