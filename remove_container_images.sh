#!/bin/bash

docker compose stop
docker compose down --volumes --remove-orphans --rmi all
echo -e "\n Listing images"
docker images -a
echo -e "\n Listing containers"
docker ps -a
echo -e "\n Listing containers"
docker volume ls
echo -e "\n Listing network"
docker network ls