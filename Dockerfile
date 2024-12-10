FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1\
    PYTHONPATH=/app

WORKDIR /APP

COPY ./requirements.txt /APP/

RUN apk add --no-cache curl

RUN pip install --no-compile --no-cache-dir  -r /APP/requirements.txt 

COPY ./monitor /APP

EXPOSE 80

ENTRYPOINT ["python3"]
CMD ["app.py"]

