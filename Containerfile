# syntax=docker/dockerfile:1
FROM python:3.13-slim

# System deps (optional: add build tools here if needed for wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifests first (better layer caching)
COPY requirements.txt requirements.txt
# If you have dev/test deps:
# COPY requirements-dev.txt requirements-dev.txt

RUN pip install --no-cache-dir -r requirements.txt
# For dev images (optional):
# RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy source
COPY . .

# Expose Gradio port
EXPOSE 7860

# Env defaults (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_PORT=7860 \
    MEMORY__ENABLED=true \
    MEMORY__BACKEND=none

# Start the app
CMD ["python", "main.py"]