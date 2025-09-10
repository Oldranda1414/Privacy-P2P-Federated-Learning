FROM alpine:latest

RUN apk add --no-cache uv

WORKDIR /app
COPY src/ ./src

ENTRYPOINT ["uv", "--project", "src", "run", "src/main/main.py"]
