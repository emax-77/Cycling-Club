# Docker deploy (Windows + Ubuntu)

## 1) Lokálne (Windows, Docker Desktop)

1. V koreňovom priečinku projektu skopíruj `.env.example` na `.env` a uprav hodnoty.
2. Spusti:
   - `docker compose up --build`
3. Aplikácia bude na `http://localhost:8000`.

Tip: ak to chceš pustiť na pozadí, použi `-d`:
- `docker compose up -d --build`

Voliteľne (v novom termináli):
- vytvor admin účet: `docker compose exec web python manage.py createsuperuser`

### Dôležité: zmena Postgres používateľa/hesla

Ak zmeníš `POSTGRES_USER` / `POSTGRES_PASSWORD` až po tom, čo sa Postgres kontajner už raz spustil, databáza ich automaticky „neprevezme“ (lebo dáta sú vo volume).

Najjednoduchšie pre lokálny vývoj:
- `docker compose down -v`
- uprav `.env`
- `docker compose up -d --build`

### Produkčný štýl: ako dostať zmeny kódu do kontajnera

V “produkčnom štýle” je kód zabalený v Docker image. Keď upravíš `.py` / templates / statické súbory, musíš **rebuildnúť image** a reštartovať `web`.

- rebuild + reštart:
   - `docker compose up -d --build`
- ak chceš reštartnúť len web:
   - `docker compose up -d --build web`

Kontrola:
- stav: `docker compose ps`
- logy webu: `docker compose logs -f web`

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

### Update/deploy na Ubuntu (produkčný štýl)

Keď nahráš nové zmeny kódu na server (napr. `git pull`), nasleduje rovnaký postup:
- `git pull`
- `docker compose up -d --build`

Poznámky:
- Kontajner `web` pri štarte automaticky spustí `migrate` + `collectstatic` (cez entrypoint), takže typicky nič ďalšie netreba.
- `docker compose down` nezmaže databázu (volume ostáva). `docker compose down -v` zmaže aj DB dáta.

Užitočné príkazy:
- zastaviť: `docker compose stop`
- znovu spustiť: `docker compose start`
- odstrániť kontajnery (bez zmazania dát): `docker compose down`
- logy: `docker compose logs -f`
- shell do webu: `docker compose exec web sh`

### Odporúčaný “release” postup (produkcia)

Toto je jednoduchý a bezpečný postup pre nasadenie novej verzie na Ubuntu server.

1) Pred nasadením
- uisti sa, že `.env` je nastavené pre produkciu (`DJANGO_DEBUG=0`, `SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`)
- (odporúčané) sprav zálohu DB volume (aspoň občas)

2) Nasadenie novej verzie
- `git pull`
- rebuild s čerstvými base images:
   - `docker compose build --pull web`
- spusti/aktualizuj služby:
   - `docker compose up -d`

Poznámka: `web` kontajner pri štarte automaticky urobí `migrate` + `collectstatic` (cez entrypoint).

3) Kontrola po nasadení
- `docker compose ps`
- `docker compose logs -f --tail=200 web`
- otvoriť web a kliknúť pár stránok / admin

4) Uvoľnenie miesta (voliteľné)
- zobraziť veľké veci: `docker image ls`
- zmazať nepoužívané images/cache:
   - `docker image prune -f`
   - `docker builder prune -f`

### Rollback (keď sa niečo pokazí)

Najjednoduchší rollback je vrátiť kód na predchádzajúci commit a znovu rebuildnúť:
- `git log --oneline --decorate -10`
- `git checkout <commit-alebo-tag>`
- `docker compose build --pull web`
- `docker compose up -d`

Ak nasadenie spravilo DB migrácie, rollback kódu môže vyžadovať aj “reverse” migrácie (to už závisí od konkrétnej zmeny). Preto je dobré robiť DB zálohy pred väčšími zmenami.

### Postgres DB backup/restore (pg_dump)

Najprenositeľnejší backup je SQL dump cez `pg_dump`.

#### Backup (Windows PowerShell)

Odporúčaný postup (dump sa vytvorí v kontajneri a skopíruje sa na host, aby sa predišlo problémom s kódovaním/redirectom v PowerShell):

- vytvor adresár:
   - `New-Item -ItemType Directory -Force backups`
- sprav dump v DB kontajneri:
   - `docker compose exec db sh -lc 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /tmp/db_backup.sql'`
- skopíruj dump na host:
   - `$dbId = docker compose ps -q db`
   - `docker cp "$dbId:/tmp/db_backup.sql" ".\\backups\\db_backup.sql"`

#### Restore (Windows PowerShell)

- (odporúčané) zastav web počas restore:
   - `docker compose stop web`
- skopíruj dump do DB kontajnera:
   - `$dbId = docker compose ps -q db`
   - `docker cp ".\\backups\\db_backup.sql" "$dbId:/tmp/db_backup.sql"`
- obnov DB:
   - `docker compose exec db sh -lc 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /tmp/db_backup.sql'`
- spusti web:
   - `docker compose start web`

#### Backup (Linux/macOS)

Tu sa dá bezpečne použiť aj shell redirect:

- `mkdir -p backups`
- `docker compose exec -T db sh -lc 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' > backups/db_backup.sql`

#### Restore (Linux/macOS)

- `docker compose stop web`
- `docker compose exec -T db sh -lc 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < backups/db_backup.sql`
- `docker compose start web`

Poznámky:
- Dump obsahuje aj dáta; pri väčších DB môže byť veľký.
- Pre “bezpečnejší” režim (compressed, rýchlejší restore) sa dá použiť aj `pg_dump -Fc` + `pg_restore`, ale na začiatok SQL dump stačí.

Poznámka:
- Pre produkciu odporúčam reverzný proxy (Nginx) a HTTPS (napr. cez Cloudflare Tunnel). V tom prípade nechaj `web` bežať interne na porte 8000 a Nginx/CF bude proxy.
