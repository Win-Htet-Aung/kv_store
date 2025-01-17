# pull official base image
FROM python:3.10.14-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip --user
COPY ./requirements.txt .
RUN pip install -r requirements.txt --user

# copy project
COPY . .
