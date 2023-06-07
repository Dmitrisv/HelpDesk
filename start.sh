python3 ./manage.py makemigrations
python3 ./manage.py migrate 
mkdir staticfiles
mkdir media
python3 ./manage.py collectstatic --noinput --clear

exec gunicorn --config python:gunicorn_config main.asgi:application