python3 ./manage.py makemigrations requesting
python3 ./manage.py migrate 
mkdir staticfiles
python3 ./manage.py collectstatic

exec gunicorn --config python:gunicorn_config main.asgi:application