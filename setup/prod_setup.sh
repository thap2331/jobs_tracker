#!/bin/bash

pg_isready -h localhost -p 5432
previous_success=$?
echo "previous_success $previous_success"

if [[ $previous_success -ne 0 ]]
then
    echo Pg is not ready. Try setting up the database again.
    exit
fi

if [[ $previous_success -eq 0 ]]
then
    echo Pg is ready
fi

python database/initialize_database.py

bash ./setup/test_setup_fill_data.sh

# docker exec jt_frontend bash -c "cd .. ; python database/initialize_database.py -r prod"
# docker exec jt_frontend bash -c "cd .. ; bash shell_scripts/fill_test_db.sh"