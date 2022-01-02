FROM python:3

ENV PYTHONBUFFERED 1

RUN mkdir /sor
WORKDIR /sor

COPY ./sor /sor

RUN pip install -r requirements.txt