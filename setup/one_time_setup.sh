#!/bin/bash

if [[ $1 == "test" ]]; then
    echo start test database
    source setenv.sh test
    docker compose up test_entrypoint test_database frontend -d

    docker exec test_box bash -c "pg_isready -d test_jt_db -h test_jt_pg_container -U postgres -p 5432"
    previous_success=$?
    echo "previous_success $previous_success"

    if [[ $previous_success -ne 0 ]]
    then
        echo Test Pg container is not ready. Wait for a few seconds and try again.
        exit
    fi

    if [[ $previous_success -eq 0 ]]
    then
        echo Test Pg container is ready.
    fi

    echo Initializing database
    docker exec test_box bash -c "python database/initialize_database.py"

    echo Filling in the data
    docker exec test_box bash -c "python3 setup/fill_data.py"


else
    echo "starting production environment"
    source setenv.sh
    docker compose up prod_entrypoint prod_database frontend -d

    docker exec prod_box bash -c "pg_isready -d jt_db -h jt_pg_container -U postgres -p 5432"
    previous_success=$?
    echo "previous_success $previous_success"

    if [[ $previous_success -ne 0 ]]
    then
        echo Production Postgres container is not ready. Wait for a few seconds and try again.
        exit
    fi

    if [[ $previous_success -eq 0 ]]
    then
        echo Production Postgres container is ready.
    fi

    echo running: python database/initialize_database.py
    docker exec prod_box bash -c "python database/initialize_database.py"

    echo running: docker exec prod_box bash -c "bash setup/fill_data.py"
    docker exec prod_box bash -c "python3 setup/fill_data.py"

fi