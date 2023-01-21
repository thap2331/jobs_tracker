docker volume create pg_vol
docker run -d --name=pg14 -p 5432:5432 -v pg_vol:/var/lib/postgresql/data -e POSTGRES_PASSWORD=pass postgres:14.6
docker exec -it pg14 psql -U postgres

psql -h localhost -U postgres