FROM python:3.8
WORKDIR /app

COPY main.py ./main.py
COPY replicas ./replicas
COPY requests ./requests
COPY state ./state
COPY Models ./Models
COPY Server ./Server

# COPY test.py ./test.py

RUN apt-get update && apt-get upgrade -y
