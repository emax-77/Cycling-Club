# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (psycopg/libpq, health checks)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Create dirs for static/media (useful when mounting volumes)
RUN mkdir -p /app/productionfiles /app/media

# Entrypoint to run migrate/collectstatic
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

# default cmd (can be overridden by docker compose)
CMD ["gunicorn", "my_ebike.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
