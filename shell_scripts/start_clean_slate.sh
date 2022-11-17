#!/bin/bash

set -e

if [ -e database/jobs.db ]
then
    rm database/jobs.db
else
    echo "No database."
fi


echo "Initializing database"
python database/initialize_database.py
python3 tracker/add_job_listing.py -u https://www.onxmaps.com/join-our-team -jt "backend engineer"
python3 tracker/add_job_listing.py -u https://www.texastribune.org/jobs/ -jt "sales-mgr" -t
# python3 tracker/add_job_listing.py -u https://jobs.intel.com/en/search-jobs -jt "insight"

# python3 tracker/add_job_listing.py -u https://careers.justeattakeaway.com/global/en/c/corporate-jobs -jt "senior pricing manager" -r

pip3 install -r requirements.txt