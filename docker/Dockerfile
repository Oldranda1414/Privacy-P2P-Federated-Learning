# Start from lightweight Alpine image
FROM alpine:latest

# Install uv
RUN apk add --no-cache uv

# Copy project
WORKDIR /app
COPY src/ ./src

# Default entrypoint (peer runs, args will be passed from docker-compose)
ENTRYPOINT ["uv", "--project", "src", "run", "src/main/main.py"]
