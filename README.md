## Installation
[Install `Docker Compose`](https://docs.docker.com/compose/install/).
### Configuration
Copy the `.env.template` file to `.env`. Set the settings you need in the `.env` file.
### Development
```bash
docker compose build
docker compose run --rm django python3 manage.py migrate
docker compose run --rm django python3 manage.py compilemessages
docker compose up
```
### Production
To run this in production, you need to specify a domain name and email settings in `.env`.
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml build
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
