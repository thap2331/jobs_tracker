import sys
sys.path.insert(0, '.')

import random
from database.data_models import CronJobsList
from database.db_configs import GetDBCreds
from database.db_manager import Ingestion

#Keep this in utils

class BuildCron:
    def __init__(self):
        self.run_mode               = GetDBCreds().get_runmode()

    def build_cron_job_commands(self, **kwargs):
        absolute_path   = kwargs.get("absolute_path")
        jobtype         = kwargs.get("jobtype")
        cronjob         = kwargs.get("cronjob")
        cronid          = kwargs.get("cronid")
        boxtype         = kwargs.get("boxtype")
        fullcronjob     = kwargs.get("fullcronjob")

        absolute_path = absolute_path.rstrip("/")
        if not jobtype:
            jobtype = "crawl"
        if not cronjob:
            cronjob = "0 * * * *"
        if not cronid:
            cronid = f"{jobtype}_{random.randint(1, 9999999)}"
        if not boxtype:
            boxtype = "linux"
        
        if jobtype == "crawl":
            fullcronjob = f'(crontab -l ; echo "{cronjob} {absolute_path}/setup/crawl/crawl_jobs.sh {self.run_mode} {absolute_path}  dup >> {absolute_path}/{self.run_mode}_crawl_cronjob.log 2>&1 #{cronid}") | sort - | uniq - | crontab -'
            delete_fullcronjob = f'crontab -l | grep -v "#{cronid}" | crontab'

        if jobtype == "email":
            fullcronjob = f'(crontab -l ; echo "{cronjob} {absolute_path}/setup/email/email_jobs.sh {absolute_path} {self.run_mode} >> {absolute_path}/{self.run_mode}_email_cronjob.log 2>&1 #{cronid}") | sort - | uniq - | crontab -'
            delete_fullcronjob = f'crontab -l | grep -v "#{cronid}" | crontab'
    
        data = {
            "absolute_path":absolute_path,
            "jobtype":jobtype,
            "cronjob":cronjob,
            "cronid":cronid,
            "boxtype":boxtype,
            "fullcronjob":fullcronjob,
            "delete_fullcronjob":delete_fullcronjob
        }

        Ingestion().insert_data(CronJobsList, data)

        return
