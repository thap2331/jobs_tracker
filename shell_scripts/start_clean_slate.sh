#!/bin/bash

set -e

if [ -e database/jobs.db ]
then
    rm database/jobs.db
else
    echo "No database."
fi

pip3 install -r requirements.txt

echo "Initializing database"
python3 database/initialize_database.py

#For developer test
python3 tracker/add_job_listing.py -u https://www.onxmaps.com/join-our-team -jt "backend engineer"
python3 tracker/add_job_listing.py -u https://www.texastribune.org/jobs/ -jt "sales-mgr" -t
python3 tracker/add_job_listing.py -u https://jobs.intel.com/en/search-jobs -jt "insight"

#Supported websites
# python3 tracker/add_job_listing.py -u https://www.onxmaps.com/join-our-team
# python3 tracker/add_job_listing.py -u https://www.texastribune.org/jobs/
# python3 tracker/add_job_listing.py -u https://jobs.intel.com/en/search-jobs

#Prep env for crawl
# sqlite3
# python3
# requirements.txt