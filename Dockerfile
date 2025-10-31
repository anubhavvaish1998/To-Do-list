FROM python:3.11-slim

WORKDIR /usr/src/To-Do List

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Entrypoint is declared in docker-compose (we run manage_startup then gunicorn there)