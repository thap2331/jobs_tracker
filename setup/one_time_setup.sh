#!/bin/bash

if [[ $1 == "test" ]]; then
    echo start test database
    source setenv.sh test
    docker compose up test_entrypoint test_database frontend -d
    bash setup/test_setup.sh

else
    echo "starting production environment"
    source setenv.sh
    docker compose up prod_entrypoint prod_database frontend -d
    bash setup/prod_setup.sh
fi