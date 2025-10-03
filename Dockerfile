## Parent image
FROM python:3.12-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies and uv
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

## Add uv to PATH
ENV PATH="/root/.cargo/bin:$PATH"

## Copying all contents from local to app
COPY . .

## Install dependencies with uv (use --system for production, not -e)
RUN uv pip install --system .

## Used PORTS
EXPOSE 8501

## Run the app 
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]