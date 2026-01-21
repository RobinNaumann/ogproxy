# Use official Python image
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

# CORS_ALLOW_ORIGINS env variable can be set at runtime
ENV ORIGINS="*"
ENV CACHE_MINUTES=60

# Expose port 80
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
