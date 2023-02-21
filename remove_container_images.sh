#!/bin/bash

docker compose stop
docker compose down --volumes --remove-orphans
# docker volume rm -f jt_pg_vol_prod jt_pg_vol_test
# docker container prune -f
# docker image prune -a -f