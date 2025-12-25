FROM python:3.11-slim

# 1️⃣ Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2️⃣ Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3️⃣ Copy app
COPY app ./app

# 4️⃣ Run service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"]