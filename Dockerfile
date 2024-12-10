FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1\
    PYTHONPATH=/app\
    PROJECT_DIRECTORY=/app

WORKDIR /app

COPY ./requirements.txt /app/

RUN apk add --no-cache curl

RUN pip install --no-compile --no-cache-dir  -r /app/requirements.txt 

COPY ./monitor /app/monitor

