#FROM ubuntu:latest
LABEL authors="sskry"

FROM python:3.13-alpine3.21

RUN apk add postgresql-client build-base postgresql-dev
COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password messenger-user

COPY messenger /messenger

WORKDIR /messenger
EXPOSE 8000



USER messenger-user