#!/bin/bash
set -e

service postgresql start
pg_lsclusters

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE DATABASE $1-raft-logs;
    GRANT CONNECT TO dev IDENTIFIED BY passwd;
EOSQL
||
echo "DB could not be created"

#// TODO - do this through pgsql dataabase docker container
