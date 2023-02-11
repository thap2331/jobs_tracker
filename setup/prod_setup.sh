#!/bin/bash

# pg_isready -p 5432 -d jt_db -h localhost -U postgres

docker exec prod_box bash -c "pg_isready -d jt_db -h jt_pg_container -U postgres -p 5432"
previous_success=$?
echo "previous_success $previous_success"

if [[ $previous_success -ne 0 ]]
then
    echo Production Postgres container is not ready. Try setting up the database again.
    exit
fi

if [[ $previous_success -eq 0 ]]
then
    echo Production Postgres container is ready.
fi

echo running: python database/initialize_database.py
docker exec prod_box bash -c "python database/initialize_database.py"

echo running: docker exec prod_box bash -c "bash setup/test_setup_fill_data.sh"
docker exec prod_box bash -c "bash setup/test_setup_fill_data.sh"
