FROM python:3-slim as python

WORKDIR /app

EXPOSE 80


COPY ./requirements.txt .
  
RUN groupadd -r django \
  && useradd -g django -r django


RUN pip install -r requirements.txt
COPY --chown=django:django . .

USER django
