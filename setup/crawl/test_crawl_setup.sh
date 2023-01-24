#!/bin/bash

docker compose down

docker compose up -d setup database_test

readonly SLEEP_TIME=5

# timeout 3 psql -h $PG_HOST -U $PG_USER -p $port -d $PG_DB -c "select 1" > /dev/null
until timeout 3 pg_isready -p 5433 -d test_jt_db -h localhost -U postgres 
do
  printf "Waiting %s seconds for PostgreSQL to come up.\n" $SLEEP_TIME
  sleep $SLEEP_TIME;
done
