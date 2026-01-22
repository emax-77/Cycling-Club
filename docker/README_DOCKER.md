# Docker deploy (Windows + Ubuntu)

## 1) Lokálne (Windows, Docker Desktop)

1. V koreňovom priečinku projektu skopíruj `.env.example` na `.env` a uprav hodnoty.
2. Spusti:
   - `docker compose up --build`
3. Aplikácia bude na `http://localhost:8000`.

Voliteľne (v novom termináli):
- vytvor admin účet: `docker compose exec web python manage.py createsuperuser`

### Dôležité: zmena Postgres používateľa/hesla

Ak zmeníš `POSTGRES_USER` / `POSTGRES_PASSWORD` až po tom, čo sa Postgres kontajner už raz spustil, databáza ich automaticky „neprevezme“ (lebo dáta sú vo volume).

Najjednoduchšie pre lokálny vývoj:
- `docker compose down -v`
- uprav `.env`
- `docker compose up -d --build`

## 2) Ubuntu server (Docker Engine)

1. Nainštaluj Docker + Compose plugin.
2. Nahraj repozitár na server (git clone / rsync).
3. Vytvor `.env` (necommitovať) a nastav aspoň:
   - `DJANGO_DEBUG=0`
   - `SECRET_KEY=...` (silný náhodný)
   - `DJANGO_ALLOWED_HOSTS=your-domain-or-ip`
   - `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain`
   - `POSTGRES_*` + `DATABASE_URL`
4. Spusti:
   - `docker compose up -d --build`

Poznámka:
- Pre produkciu odporúčam reverzný proxy (Nginx) a HTTPS (napr. cez Cloudflare Tunnel). V tom prípade nechaj `web` bežať interne na porte 8000 a Nginx/CF bude proxy.
