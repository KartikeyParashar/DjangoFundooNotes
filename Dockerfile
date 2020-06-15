# pull official base image
FROM python:3

# set work directory
RUN mkdir FUNDOOAPP
WORKDIR /FUNDOOAPP

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /FUNDOOAPP/requirements.txt
RUN pip install -r requirements.txt



# copy project
COPY . /FUNDOOAPP

EXPOSE 8000