FROM python:3-slim as python

WORKDIR /app

EXPOSE 8000


COPY ./requirements.txt .
  
RUN groupadd -r django \
  && useradd -g django -r django


RUN pip install -r requirements.txt
COPY --chown=django:django . .
RUN chown -R django:django /usr/local/lib/python3.11/site-packages/two_factor/migrations/

USER django
