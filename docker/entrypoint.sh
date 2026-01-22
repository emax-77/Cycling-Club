#!/usr/bin/env sh
set -e

# Optional: wait for Postgres if DATABASE_URL points at it
if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database..."
  python - <<'PY'
import os
import time
import sys

import dj_database_url
import psycopg

url = os.environ.get("DATABASE_URL")
config = dj_database_url.parse(url)
# dj_database_url returns NAME/USER/PASSWORD/HOST/PORT
host = config.get("HOST")
port = int(config.get("PORT") or 5432)
dbname = config.get("NAME")
user = config.get("USER")
password = config.get("PASSWORD")

# Keep it simple: assume non-SSL in local docker unless required by env
sslmode = "require" if os.environ.get("DJANGO_DB_SSL_REQUIRE", "").strip().lower() in {"1","true","yes","y","on"} else "disable"

deadline = time.time() + 60
while True:
    try:
        with psycopg.connect(host=host, port=port, dbname=dbname, user=user, password=password, sslmode=sslmode, connect_timeout=3):
            break
    except Exception as exc:
        if time.time() > deadline:
            print(f"Database not ready after 60s: {exc}", file=sys.stderr)
            raise
        time.sleep(1)
print("Database is ready")
PY
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"
