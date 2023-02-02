#!/bin/bash

#make it available for both test and prod

docker compose up database_test test_entrypoint -d
docker exec test_box bash -c "python email_utils/send_email_utils.py"
docker compose down