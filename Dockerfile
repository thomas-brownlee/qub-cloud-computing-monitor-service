FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1\
    PYTHONPATH=/app\
    PROJECT_DIRECTORY=/app\
    CLUSTER_NETWORK="cluster_docker-network"\
    GITLAB_URL=https://repository.hal.davecutting.uk/\
    PROJECT_ID=6546\
    GITLAB_TOKEN=glpat-wf2KZrJyYhEQx-tbKUiS

WORKDIR /app

COPY ./requirements.txt /app/

RUN apk add --no-cache curl

RUN pip install --no-compile --no-cache-dir  -r /app/requirements.txt 

COPY ./monitor /app/monitor

EXPOSE 80
CMD ["python", "/app/monitor/src/app.py"]