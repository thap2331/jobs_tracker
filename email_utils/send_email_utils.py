import sys
sys.path.insert(0, '.')

from email_utils.email_login import NotifyNewJobs
from database.data_models import CronLogs
from database.db_manager import Ingestion
from datetime import datetime

current_utc_time = datetime.now()
Ingestion().insert_data(table=CronLogs, data={
    "info":"cron send email", 
    "last_attempted_crawl":current_utc_time
    })

NotifyNewJobs().notify_new_jobs()