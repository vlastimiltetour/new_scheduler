FROM python:3.11-slim

WORKDIR /app

# Instalace závislostí
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování kódu aplikace
COPY . .

# Expozice portu (standardně 8000)
EXPOSE 8000

# Produkční spuštění Uvicornu (bez --reload, s více workery)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]