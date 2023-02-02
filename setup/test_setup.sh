#!/bin/bash

# localbox
# pg_isready -p 5433 -d test_jt_db -h localhost -U postgres

docker exec test_box bash -c "pg_isready -d test_jt_db -h test_jt_pg_container -U postgres -p 5432"
previous_success=$?
echo "previous_success $previous_success"

if [[ $previous_success -ne 0 ]]
then
    echo Test Pg container is not ready. Try setting up the database again.
    exit
fi

if [[ $previous_success -eq 0 ]]
then
    echo Test Pg container is ready.
fi

echo running: python database/initialize_database.py
docker exec test_box bash -c "python database/initialize_database.py"

echo running: docker exec test_box bash -c "bash setup/test_setup_fill_data.sh"
docker exec test_box bash -c "bash setup/test_setup_fill_data.sh"

# conn_string='host=test_jt_pg_container dbname=test_jt_db user=postgres password=pass port=5432'