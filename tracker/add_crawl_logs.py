import sys
sys.path.insert(0, '.')


from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timedelta
import pytz, argparse

from database.db_manager import DBConnect
from database.data_models import Jobs, CrawlLogs, JobListingMeta
from scraping.pipeline import Ingestion
from database.data_models import CrawlLogs

parser = argparse.ArgumentParser()
parser.add_argument('--test_data', '-t', nargs='?', required=False, help='add test data')

class AddCrawlLogs:

    def add_crawl_logs(self, data, time=None):
        url = data.get("url")
        if time:
            pst_timenow=time
        else:
            pst_timenow = self.get_pst_timenow()
        values = (url, pst_timenow)
        stmt = "INSERT INTO crawlogs (url, last_attempted_crawl) VALUES (%s,%s) ON CONFLICT (url) DO UPDATE SET last_attempted_crawl = excluded.last_attempted_crawl"

        DBConnect().sql_execute_statement(stmt, values)
        return

    def add_test_data(self, data=None):
        print("Adding test data")
        #convert data and upload it if given - take a list of dict and loop and upload it
        self.add_crawl_logs({"url":"url.com"}, time=self.get_pst_timenow())

        #two days ago
        utc_now = pytz.utc.localize(datetime.utcnow())
        now = utc_now.astimezone(pytz.timezone("US/Pacific"))
        pst_time_two_days_ago = now - timedelta(days=2)
        self.add_crawl_logs({"url":"url2.com"},time=pst_time_two_days_ago)

        return

    def get_pst_timenow(self):
        utc_now = pytz.utc.localize(datetime.utcnow())
        timenow = utc_now.astimezone(pytz.timezone("US/Pacific"))

        return timenow

if __name__ == "__main__":
    args = parser.parse_args()
    if args.test_data:
        AddCrawlLogs().add_test_data()