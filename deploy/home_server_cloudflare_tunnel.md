# Home server via Cloudflare Tunnel (step-by-step)

This approach works even with dynamic IP and often even with CGNAT.
Cloudflare terminates TLS and forwards traffic to your home server.

## Two modes

### Mode 1 (no domain): quick temporary URL
Good for testing only.
- Install `cloudflared`
- Run (direct to Gunicorn): `cloudflared tunnel --url http://127.0.0.1:8000`
- Or (recommended, via local Nginx on 8080): `cloudflared tunnel --url http://127.0.0.1:8080`
- You will get a `https://<random>.trycloudflare.com` URL

Limits:
- Hostname changes every run
- Hard to keep Django `ALLOWED_HOSTS` + CSRF stable

### Mode 2 (recommended): stable hostname with a domain
- Buy any cheap domain (can be later)
- Put DNS on Cloudflare (free)
- Create a named tunnel and map a hostname to your local service

## Server layout recommendation
- Run Django via Gunicorn bound to `127.0.0.1:8000`
- Put Nginx in front locally and bind it to `127.0.0.1:8080`
	- This matters because with `DJANGO_DEBUG=0`, Django will not serve `/media/` by itself
- Cloudflared connects to localhost only (no router port forwarding)

## Django env vars (production)
Set these on the server:
- `DJANGO_DEBUG=0`
- `SECRET_KEY=<long random>`
- `DJANGO_ALLOWED_HOSTS=your-hostname.example.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-hostname.example.com`
- `DATABASE_URL=postgres://...` (recommended)
- SMTP: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

## Linux (Ubuntu) quick commands (domain-based tunnel)
1) Install cloudflared
- `wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb`
- `sudo dpkg -i cloudflared-linux-amd64.deb`

2) Authenticate
- `cloudflared tunnel login`

3) Create tunnel
- `cloudflared tunnel create cycling-club`

4) Create DNS route (hostname -> tunnel)
- `cloudflared tunnel route dns cycling-club your-hostname.example.com`

5) Config file
- Put config at `/etc/cloudflared/config.yml` (see `deploy/cloudflared-config.yml`)
- Ensure `tunnel:` and `credentials-file:` are set correctly

6) Run as service
- Create user: `sudo useradd -r -s /usr/sbin/nologin cloudflared`
- `sudo mkdir -p /etc/cloudflared`
- Copy credentials JSON to `/etc/cloudflared/` and `chown cloudflared:cloudflared`
- Copy service file from `deploy/cloudflared.service` to `/etc/systemd/system/cloudflared.service`
- `sudo systemctl daemon-reload`
- `sudo systemctl enable --now cloudflared`

## Windows notes
You can run cloudflared interactively or install it as a Windows service.
For a first test (no domain):
- Download cloudflared.exe
- Run: `cloudflared.exe tunnel --url http://127.0.0.1:8000`

## Hardening (recommended)
- Enable Cloudflare Access (Zero Trust) to require login for `/admin/`.
- Keep Django bound to localhost only.
- Back up Postgres + `media/`.
