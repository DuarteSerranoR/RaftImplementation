FROM python:3.8
WORKDIR /app

COPY main.py ./main.py
COPY replicas ./replicas
COPY test.py ./test.py
COPY Models ./Models
COPY Server ./Server

RUN apt-get update && apt-get upgrade -y
