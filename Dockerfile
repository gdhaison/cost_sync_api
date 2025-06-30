# Dockerfile for Flask app
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

ENV PYTHONUNBUFFERED=1 

ENV FLASK_APP=main.py

CMD bash -c "echo '=== Running migration ===' && flask db upgrade && echo '=== Starting Gunicorn ===' && gunicorn -w 4 -b 0.0.0.0:10000 main:app"
