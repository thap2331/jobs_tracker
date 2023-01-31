#!/bin/bash

export run_mode=test
docker compose stop
docker compose down --volumes
docker container prune -f
docker image prune -a -f