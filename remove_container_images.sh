docker compose stop
docker compose down --volumes
docker container prune -f
docker image prune -a -f
