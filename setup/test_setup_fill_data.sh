#!/bin/bash


#For developer test
python3 tracker/add_job_listing.py -u https://www.onxmaps.com/join-our-team -jt "backend engineer"
python3 tracker/add_job_listing.py -u https://www.texastribune.org/jobs/ -jt "sales-mgr;director-audience-growth-engagement" -t
python3 tracker/add_job_listing.py -u https://jobs.intel.com/en/search-jobs -jt "insight"

python3 tracker/add_crawl_logs.py -t add