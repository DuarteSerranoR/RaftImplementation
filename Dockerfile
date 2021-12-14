FROM postgres:9.4
ARG DB_NAME
WORKDIR /app

COPY dbsetup.sh ./dbsetup.sh
RUN ./dbsetup.sh $DB_NAME

COPY main.py ./main.py
COPY DB ./DB
COPY Models ./Models
COPY Server ./Server
COPY replicas ./replicas

# COPY test.py ./test.py

RUN apt-get update && apt-get upgrade -y
