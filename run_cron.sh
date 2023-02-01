#!/bin/bash

# readonly SLEEP_TIME=5

# until timeout 3 pg_isready -p 5433 -d test_jt_db -h localhost -U postgres 
# do
#   printf "Waiting %s seconds for PostgreSQL to come up.\n" $SLEEP_TIME
#   sleep $SLEEP_TIME;
# done

docker exec setup_box bash -c "bash setup/crawl/test_crawl.sh dup"

# (crontab -l ; echo "0 * * * * /home/suraj/personal_projects/jobs_tracker/run_cron.sh #testcrawl") | sort - | uniq - | crontab -
# (crontab -l ; echo "0,5,10,15,20,25,30,35,40,45,50,55 * * * * /home/suraj/personal_projects/jobs_tracker/run_cron.sh #testcrawl") | sort - | uniq - | crontab -
# crontab -l | grep -v '#testcrawl' | crontab