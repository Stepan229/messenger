
FROM python:3.13-alpine3.21
LABEL authors="sskry"

RUN apk add postgresql-client build-base postgresql-dev

RUN mkdir -p /temp
COPY requirements.txt /temp/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /temp/requirements.txt

RUN adduser --disabled-password messenger-user

WORKDIR /messenger
COPY messenger /messenger


EXPOSE 8000



USER messenger-user