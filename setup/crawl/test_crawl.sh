#!/bin/bash

readonly SLEEP_TIME=5

until timeout 3 pg_isready -p 5433 -d test_jt_db -h localhost -U postgres 
do
  printf "Waiting %s seconds for PostgreSQL to come up.\n" $SLEEP_TIME
  sleep $SLEEP_TIME;
done

