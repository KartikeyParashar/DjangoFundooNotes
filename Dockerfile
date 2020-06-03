FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /FUNDOOAPP

ADD . /FUNDOOAPP

COPY ./requirements.txt /FUNDOOAPP/requirements.txt

RUN pip install -r requirements.txt

COPY . /FUNDOOAPP

