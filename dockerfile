FROM python:3.11-slim

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code app copying
COPY . .

# Port Exposure
EXPOSE 8080

# Production univcorn env
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]