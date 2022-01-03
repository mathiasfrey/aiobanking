FROM python:3

ENV PYTHONBUFFERED 1

COPY ./sor/requirements.txt .
RUN pip install -r requirements.txt

ADD ./sor .