python3 ./manage.py makemigrations requesting
python3 ./manage.py migrate 
mkdir staticfiles
python3 ./manage.py collectstatic --noinput --clear

exec gunicorn --config python:gunicorn_config main.asgi:application