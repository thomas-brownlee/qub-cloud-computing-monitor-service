FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1\
    PYTHONPATH=/app\
    PROJECT_DIRECTORY=/app\
    CLUSTER_NETWORK="cluster_docker-network"

WORKDIR /app

COPY ./requirements.txt /app/

RUN apk add --no-cache curl

RUN pip install --no-compile --no-cache-dir  -r /app/requirements.txt 

COPY ./monitor /app/monitor

CMD ["python", "/app/monitor/src/app.py"]