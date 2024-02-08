FROM python:3.11.3-slim-buster
LABEL author="vitalii-babiienko"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt

COPY . .
