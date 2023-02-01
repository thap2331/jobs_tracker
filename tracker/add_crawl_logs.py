import sys
sys.path.insert(0, '.')


from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timedelta
import pytz, argparse

from database.db_manager import DBConnect, Ingestion
from database.data_models import Jobs, CrawlLogs, JobListingMeta

parser = argparse.ArgumentParser()
parser.add_argument('--test_data', '-t', nargs='?', required=False, help='add test data')

class AddCrawlLogs:
    def __init__(self,) -> None:
        self.db_connect = DBConnect()
        self.ingestion = Ingestion()

    def pg_upsert_crawl_logs(self, data, time=None):
        url = data.get("url")
        if time:
            pst_timenow=time
        else:
            pst_timenow = self.get_pst_timenow()
        values = (url, pst_timenow)
        stmt = "INSERT INTO crawlogs (url, last_attempted_crawl) VALUES (%s,%s) ON CONFLICT (url) DO UPDATE SET last_attempted_crawl = excluded.last_attempted_crawl"

        DBConnect().sql_execute_statement(stmt, values)
        return

    def add_crawl_logs(self, data):
        if not isinstance(data, dict) or not isinstance(data, list):
            print(f"Data ({data}) is neither a dict nor a list.")
        
        #If data is a list
        are_dict = True
        if isinstance(data, list):
            #all inside should be a dict
            are_dict = all([isinstance(i, dict) for i in data])

        if not are_dict:
            print(f"All data inside a list ({data}) are not a dict.")
            return

        #If data is a dict
        if isinstance(data, dict):
            if not data.get("last_attempted_crawl"):
                data["last_attempted_crawl"]=datetime.now()

            data = [data]

        self.ingestion.insert_using_engine(CrawlLogs, data)
        
        return


    def add_test_data(self, data=None):
        print("Adding test data for crawl logs.")
        
        #convert data and upload it if given - take a list of dict and loop and upload it
        self.add_crawl_logs({"url":"url1.com"})

        #two days ago
        utc_now = pytz.utc.localize(datetime.utcnow())
        now = utc_now.astimezone(pytz.timezone("US/Pacific"))
        pst_time_two_days_ago = now - timedelta(days=2)
        self.add_crawl_logs({"url":"url2.com", "last_attempted_crawl":pst_time_two_days_ago})

        return

    def get_pst_timenow(self):
        utc_now = pytz.utc.localize(datetime.utcnow())
        timenow = utc_now.astimezone(pytz.timezone("US/Pacific"))

        return timenow

if __name__ == "__main__":
    args = parser.parse_args()
    if args.test_data:
        AddCrawlLogs().add_test_data()