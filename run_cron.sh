#!/bin/bash


cd /home/suraj/personal_projects/jobs_tracker/
source setenv.sh test
bash setup/crawl/test_crawl.sh dup

# (crontab -l ; echo "0 * * * * /home/suraj/personal_projects/jobs_tracker/run_cron.sh #testcrawl") | sort - | uniq - | crontab -
# (crontab -l ; echo "0,5,10,15,20,25,30,35,40,45,50,52,55 * * * * /home/suraj/personal_projects/jobs_tracker/run_cron.sh >> /home/suraj/personal_projects/jobs_tracker/test_crawl.log 2>&1 #testcrawl") | sort - | uniq - | crontab -
# crontab -l | grep -v '#testcrawl' | crontab

#every 2 mins
# (crontab -l ; echo "0,2,5,7,10,13,15,17,20,23,25,27,30,32,35,37,40,43,45,47,50,52,55,57 * * * * /home/suraj/personal_projects/jobs_tracker/run_cron.sh >> /home/suraj/personal_projects/jobs_tracker/$EPOCHSECONDS_test_crawl.log 2>&1 #testcrawl") | sort - | uniq - | crontab -