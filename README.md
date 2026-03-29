# HelpDesk

An internal IT helpdesk system built with Django. Designed to streamline support request management within a company — employees submit tickets, support staff processes them in real time.

## Stack

- **Backend:** Python, Django, Django Channels (WebSocket)
- **Frontend:** Bootstrap 5, JavaScript, CKEditor (rich text), Plotly (charts)
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose, Nginx, Gunicorn + Uvicorn (ASGI)
- **Auth:** Django two-factor authentication

## Features

- 📋 **Ticket system** — employees create support requests with rich text descriptions and file attachments
- 🔄 **Real-time updates** — ticket status changes are pushed via WebSocket without page reload
- 📊 **Dashboard** — statistics and charts (Plotly) for support staff
- 🔐 **Two-factor authentication** — 2FA for secure access
- 🖼️ **Image processing** — attachment handling via Pillow + django-imagekit
- 🎨 **Custom admin panel** — django-jazzmin for a clean admin UI
- 🐳 **Production-ready deployment** — full Docker Compose stack out of the box

## Architecture

```
User → Nginx → Gunicorn (HTTP) → Django
                    ↘ Uvicorn (ASGI/WebSocket) → Django Channels
                              ↓
                         PostgreSQL
```

Static files and media are served by Nginx directly, bypassing Django.

## Quick Start

**Requirements:** [Docker & Docker Compose](https://docs.docker.com/compose/install/)

```bash
# 1. Clone the repo
git clone https://github.com/Dmitrisv/HelpDesk.git
cd HelpDesk

# 2. Configure environment
cp .env.template .env
# Edit .env — set DB credentials, SECRET_KEY, etc.

# 3. Build and run
docker compose build
docker compose run --rm django python3 manage.py migrate
docker compose run --rm django python3 manage.py createsuperuser
docker compose up
```

App will be available at **http://localhost**

## Configuration

All settings are managed via `.env`. Copy `.env.template` and fill in the values:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for dev, `False` for prod |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |

## Project Structure

```
HelpDesk/
├── main/           # Core app — auth, users, base models
├── requesting/     # Ticket creation and management
├── dashboard/      # Analytics and statistics for staff
├── nginx-conf.d/   # Nginx configuration
├── Dockerfile
├── Docker-compose.yaml
├── gunicorn_config.py
└── start.sh        # Container entrypoint
```

## Development

Pre-commit hooks are configured for code quality:

```bash
pip install pre-commit
pre-commit install
```
