# Deployment (Django) – VPS + Home server options

This project is a small Django app with user auth, SMTP email, and media uploads.
For best price/performance and reliability, prefer a cheap VPS (Hetzner/OVH).
Home-server hosting is possible, but comes with networking and uptime caveats.

## Recommended: VPS (best price/performance)

### 0) What you need
- Ubuntu VPS (1 vCPU / 2GB RAM is usually enough)
- A public IPv4 address (most VPS provide this)
- Optional domain later (you can start with the VPS IP)

### 1) Server baseline
On the VPS:
- Create a non-root user, enable SSH keys, disable password SSH
- `ufw allow OpenSSH`, `ufw allow 80`, `ufw allow 443`, then `ufw enable`
- Install packages: Python, venv, Nginx, Postgres, build tools

### 2) Postgres
- Create DB + user for the app
- Set `DATABASE_URL` (see `.env.example`)

### 3) App runtime (Gunicorn + systemd)
- Put code in e.g. `/srv/cycling-club/`
- Create venv: `python3 -m venv .venv`
- Install deps: `pip install -r requirements.txt`
- Set environment variables in a systemd drop-in or `.env` loaded by the service
- Run:
  - `python manage.py migrate`
  - `python manage.py collectstatic --noinput`
- Run Gunicorn as a systemd service listening on a unix socket

### 4) Nginx reverse proxy
- Proxy `/` to Gunicorn socket
- Serve `/static/` from `productionfiles/`
- Serve `/media/` from `media/`

### 5) TLS (HTTPS)
- Without a domain, Let’s Encrypt is awkward (needs hostname).
- When you add a domain, use `certbot --nginx` for a free certificate.

## Alternative: Home server

### Realistic constraints
- Without a static IP, your public endpoint changes.
- Many ISPs use CGNAT (no inbound ports possible).
- Power/network outages become your uptime.

### Option A (best for dynamic IP / CGNAT): Cloudflare Tunnel
This avoids port-forwarding and static IP.
- Create a free Cloudflare account
- For a quick test without a domain, you can run a temporary `trycloudflare.com` URL
- For a stable setup, add a domain to Cloudflare and route a hostname to your tunnel
- Install `cloudflared` on your home server
- Create a tunnel that forwards `https://your-public-hostname` → `http://127.0.0.1:8000` (or your local Nginx)
- Cloudflare terminates TLS for you

See `deploy/home_server_cloudflare_tunnel.md` for step-by-step instructions.

### Option B: DDNS + Port forwarding
Works only if you have a real public IPv4.
- Use DuckDNS / No-IP to get a stable hostname
- Configure your router to forward ports 80/443 to your server
- Use Let’s Encrypt with that hostname

### Home server recommendation
Use home server as staging/backup first. For a public app, VPS is usually simpler and more reliable.

## Django production checklist (this repo)

Already applied in code:
- DEBUG controlled by `DJANGO_DEBUG`
- Debug toolbar enabled only in DEBUG
- `SECRET_KEY` required in production
- `DJANGO_ALLOWED_HOSTS` required in production
- Static files handled via WhiteNoise
- Postgres supported via `DATABASE_URL`

Still your responsibility:
- Create strong `SECRET_KEY`
- Use Postgres for production (recommended)
- Ensure `MEDIA_ROOT` is on persistent storage + backups
- Configure SMTP credentials (Gmail: App Password)

## Quick commands (typical)
- Migrations: `python manage.py migrate`
- Static: `python manage.py collectstatic --noinput`
- Run (prod style): `gunicorn my_ebike.wsgi:application --bind 127.0.0.1:8000`

## Docker (Windows + Ubuntu)

If you prefer Docker (recommended for consistency between Windows dev and Ubuntu server):
- Use `docker-compose.yml` (Django + Postgres)
- Copy `.env.example` → `.env` and fill in the values

Step-by-step guide: `docker/README_DOCKER.md`
