# Stage 1: Build Go Engine
FROM golang:1.22-alpine AS engine-builder
WORKDIR /build
COPY engine/go.mod ./
# COPY engine/go.sum ./
RUN go mod download
COPY engine/ .
RUN go build -o engine-bin ./main.go

# Stage 2: Go Runtime
FROM alpine:3.19 AS engine
WORKDIR /app
COPY --from=engine-builder /build/engine-bin .
EXPOSE 8080
CMD ["./engine-bin"]

# Stage 3: Python API
FROM python:3.11-slim AS api
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/app ./app
COPY api/main.py .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
