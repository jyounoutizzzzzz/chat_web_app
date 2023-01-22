# Dockerfile
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y vim less sudo 
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /app
COPY ./app /app

ARG USERNAME=***
ARG GROUPNAME=***
ARG UID=***
ARG GID=***
ARG PASSWORD=***
RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/bash -u $UID -g $GID $USERNAME && \
    echo $USERNAME:$PASSWORD | chpasswd && \
    usermod -aG sudo $USERNAME
USER $USERNAME
WORKDIR /app