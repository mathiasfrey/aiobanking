FROM python:3.9

ENV PYTHONBUFFERED 1

COPY ./soa/requirements.txt .
RUN pip install -r requirements.txt

ADD ./soa .

