# VPS quick setup notes (Ubuntu)

## Packages
- `sudo apt update`
- `sudo apt install -y python3 python3-venv python3-pip nginx postgresql postgresql-contrib`

## App directory
- `/srv/cycling-club` (owned by deploy user)

## Run steps
- create venv: `python3 -m venv .venv`
- install: `pip install -r requirements.txt`
- env file: `/etc/cycling-club.env` (chmod 600)
- migrate + collectstatic
- systemd: copy `deploy/gunicorn.service` to `/etc/systemd/system/cycling-club.service`
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable --now cycling-club`

## Nginx
- copy `deploy/nginx_site.conf` to `/etc/nginx/sites-available/cycling-club`
- `sudo ln -s /etc/nginx/sites-available/cycling-club /etc/nginx/sites-enabled/`
- `sudo nginx -t; sudo systemctl reload nginx`

## TLS
- with domain: `sudo apt install -y certbot python3-certbot-nginx`
- `sudo certbot --nginx -d yourdomain -d www.yourdomain`
