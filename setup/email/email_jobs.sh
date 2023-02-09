#!/bin/bash

# cd /home/usr/personal_projects/jobs_tracker/

if [[ $# -ne 2 ]]; then
    echo "Two args required. First: run mode, second: absolute path for repo."
    exit
fi

cd $1
source setenv.sh $2

if [[ $2 == "test" ]]; then
    docker compose up test_database test_entrypoint -d
    docker exec test_box bash -c "python email_utils/send_email_utils.py"
    docker compose down

elif [[ $2 == "prod" ]]; then
    docker compose up prod_database prod_entrypoint -d
    docker exec test_box bash -c "python email_utils/send_email_utils.py"
    docker compose down

fi