# data-preparer/Dockerfile
# --------------------------------------------------------------------
# Minimal container image for the Data-Preparer FastAPI microservice.
# - Uses Python slim image.
# - Installs requirements and copies app.
# - Entrypoint runs uvicorn.
# --------------------------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

# system deps for psycopg2 and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
