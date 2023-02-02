#!/bin/bash

#make it available for both test and prod in the future

#Figure out how to cd to relative path; need to delete this absolute strategy
cd /home/suraj/personal_projects/jobs_tracker/
source setenv.sh test

docker compose up database_test test_entrypoint -d
docker exec test_box bash -c "python email_utils/send_email_utils.py"
docker compose down