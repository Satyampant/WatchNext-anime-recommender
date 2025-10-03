## Parent image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copying all contents from local to app
COPY . .

## Install dependencies with uv (already in PATH)
RUN uv pip install --system .

## Used PORTS
EXPOSE 8501

## Run the app 
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]