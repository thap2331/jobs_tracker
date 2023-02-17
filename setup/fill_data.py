import sys
sys.path.insert(0,'.')

import json, pytz
from datetime import datetime,timedelta
from database.db_configs import GetDBCreds
from database.db_manager import Ingestion
from database.data_models import JobListingMeta, CrawlLogs

run_mode = GetDBCreds().get_runmode()
ingestion = Ingestion()

print("run_mode: ",run_mode)
with open("./setup/sample_data.json", "r") as f:
    data = json.load(f)


if run_mode == "test":
    data = data.get("test")

    #JobListing data
    joblisting_data = data.get("joblisting")
    ingestion.insert_data(JobListingMeta, joblisting_data)

    #Crawlogs
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = utc_now.astimezone(pytz.timezone("US/Pacific"))
    pst_time_two_days_ago = now - timedelta(days=2)
    data["crawlogs"][1]["last_attempted_crawl"]=pst_time_two_days_ago
    data["crawlogs"][0]["last_attempted_crawl"]=now
    crawl_data = data.get("crawlogs")
    ingestion.insert_data(CrawlLogs, crawl_data)

else:
    data = data.get("prod")
    
    #JobListing data
    joblisting_data = data.get("joblisting")
    ingestion.insert_data(JobListingMeta, joblisting_data)

    #Crawlogs
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = utc_now.astimezone(pytz.timezone("US/Pacific"))
    pst_time_two_days_ago = now - timedelta(days=2)
    data["crawlogs"][0]["last_attempted_crawl"]=now
    crawl_data = data.get("crawlogs")
    ingestion.insert_data(CrawlLogs, crawl_data)
    