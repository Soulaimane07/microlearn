# model-selector/Dockerfile
# --------------------------------------------------------------------
# Container image for the Model-Selector FastAPI microservice.
# - Uses Python slim image.
# - Installs requirements and copies app.
# - Entrypoint runs uvicorn.
# --------------------------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

# System deps for psycopg2, scikit-learn, and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev libgomp1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
