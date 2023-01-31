#!/bin/bash

source setenv.sh test
docker compose down
docker compose up setup database_test -d

readonly SLEEP_TIME=5

until timeout 3 pg_isready -p 5433 -d test_jt_db -h localhost -U postgres 
do
  printf "Waiting %s seconds for PostgreSQL to come up.\n" $SLEEP_TIME
  sleep $SLEEP_TIME;
done

docker exec setup_box bash -c "python scraping/crawl.py -c r"
# (crontab -l ; echo "0 * * * *  'Hello Suraj fron cron job'>>/home/suraj/personal_projects/learn/cronjobs/cronlogs.txt #hellosuraj") | sort - | uniq - | crontab -

# (crontab -l ; echo "0 * * * * /home/suraj/personal_projects/jobs_tracker/run_cron.sh #hellosuraj") | sort - | uniq - | crontab -

docker compose down