import sys
sys.path.insert(0, '.')

import random
from database.data_models import CronJobsList
from database.db_configs import GetDBCreds
from database.db_manager import Ingestion

class BuildCron:
    def __init__(self):
        self.run_mode = GetDBCreds().get_runmode()

    def given_cols(self, **kwargs):
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
        
        if self.run_mode == "test":
            if jobtype == "crawl":
                fullcronjob = f'(crontab -l ; echo "{cronjob} {absolute_path}/setup/crawl/test_crawl.sh dup {absolute_path} >> {absolute_path}/test_crawl_cronjob.log 2>&1 #{cronid}") | sort - | uniq - | crontab -'
                delete_fullcronjob = f'crontab -l | grep -v "#{cronid}" | crontab'

            if jobtype == "email":
                pass
    
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
