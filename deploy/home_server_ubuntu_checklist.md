# Ubuntu Server home deployment (Cloudflare Tunnel)

This checklist assumes:
- Ubuntu Server on your old PC
- You will use Cloudflare Tunnel (no router port-forward)
- You need auth/email and uploaded images in `media/`

## 1) Create a deploy user + basic hardening
```bash
sudo adduser deploy
sudo usermod -aG sudo deploy

# optional but recommended
sudo apt update
sudo apt install -y ufw
sudo ufw allow OpenSSH
sudo ufw enable
```

## 2) Install system packages
```bash
sudo apt update
sudo apt install -y \
  python3 python3-venv python3-pip \
  nginx \
  postgresql postgresql-contrib \
  git
```

## 3) Get the code onto the server
Example:
```bash
sudo mkdir -p /srv/cycling-club
sudo chown deploy:deploy /srv/cycling-club

# as deploy user
cd /srv/cycling-club
git clone <YOUR_REPO_URL> .
```

## 4) Python venv + dependencies
```bash
cd /srv/cycling-club
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## 5) Postgres (recommended)
```bash
sudo -u postgres psql
```
Inside psql:
```sql
CREATE DATABASE cyclingclub;
CREATE USER cyclingclub_user WITH PASSWORD 'CHANGE_ME';
ALTER ROLE cyclingclub_user SET client_encoding TO 'utf8';
ALTER ROLE cyclingclub_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cyclingclub_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cyclingclub TO cyclingclub_user;
\q
```

Your `DATABASE_URL` will look like:
`postgres://cyclingclub_user:CHANGE_ME@127.0.0.1:5432/cyclingclub`

## 6) Create environment file
Create `/etc/cycling-club.env`:
```bash
sudo nano /etc/cycling-club.env
sudo chmod 600 /etc/cycling-club.env
```
Example contents (adapt):
```ini
DJANGO_DEBUG=0
SECRET_KEY=CHANGE_ME_TO_LONG_RANDOM
DJANGO_ALLOWED_HOSTS=your-hostname.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-hostname.example.com

DATABASE_URL=postgres://cyclingclub_user:CHANGE_ME@127.0.0.1:5432/cyclingclub

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=you@gmail.com
EMAIL_HOST_PASSWORD=GMAIL_APP_PASSWORD
CONTACT_RECIPIENT_EMAIL=you@gmail.com
```

## 7) Django migrate + static
```bash
cd /srv/cycling-club
source .venv/bin/activate

# sanity check
python manage.py check --deploy

python manage.py migrate
python manage.py collectstatic --noinput
```

## 8) Run Gunicorn as a service
- Copy `deploy/gunicorn.service` to `/etc/systemd/system/cycling-club.service`
- Edit paths + use EnvironmentFile

Example:
```bash
sudo cp /srv/cycling-club/deploy/gunicorn.service /etc/systemd/system/cycling-club.service
sudo nano /etc/systemd/system/cycling-club.service
```
Make sure you have:
- `WorkingDirectory=/srv/cycling-club`
- `ExecStart=/srv/cycling-club/.venv/bin/gunicorn ... --bind 127.0.0.1:8000`
- `EnvironmentFile=/etc/cycling-club.env`

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cycling-club
sudo systemctl status cycling-club --no-pager
```

## 9) Nginx (local-only) to serve /media/
Important: with `DJANGO_DEBUG=0`, Django will NOT serve `/media/` by itself.

Use the local-only config `deploy/nginx_cloudflare_local.conf`:
```bash
sudo cp /srv/cycling-club/deploy/nginx_cloudflare_local.conf /etc/nginx/sites-available/cycling-club
sudo ln -sf /etc/nginx/sites-available/cycling-club /etc/nginx/sites-enabled/cycling-club
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

Nginx listens on `127.0.0.1:8080` only.

## 10) Cloudflare Tunnel
### Quick test (no domain)
```bash
# install cloudflared (Ubuntu)
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# point tunnel to local nginx
cloudflared tunnel --url http://127.0.0.1:8080
```

### Stable setup (with domain)
Follow `deploy/home_server_cloudflare_tunnel.md` and point ingress to:
- `service: http://127.0.0.1:8080`

## 11) Backups (minimum)
- Back up Postgres daily
- Back up `/srv/cycling-club/media/`

Example pg dump:
```bash
sudo -u postgres pg_dump cyclingclub | gzip > /srv/cycling-club/backups/db_$(date +%F).sql.gz
```

## Troubleshooting
- App logs: `sudo journalctl -u cycling-club -f`
- Nginx logs: `/var/log/nginx/access.log` and `error.log`
- Check headers/hosts: ensure `DJANGO_ALLOWED_HOSTS` matches your tunnel hostname
