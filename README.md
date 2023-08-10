## Installation
[Install `Docker Compose`](https://docs.docker.com/compose/install/).
### Configuration
Copy the `.env.template` file to `.env`. Set the settings you need in the `.env` file.
### Development
```bash
docker compose build
docker compose run --rm django python3 manage.py makemigrations
docker compose run --rm django python3 manage.py migrate
docker compose up
```
