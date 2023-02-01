import sys
sys.path.insert(0, '.')

import inspect, importlib, pytz, argparse
from datetime import datetime, timedelta

from database.data_models import Jobs, CrawlLogs, CronLogs, JobListingMeta
from database.db_manager import DBConnect
from scraping.utils.crawl_utils import Crawl
from tracker.add_crawl_logs import AddCronLogs

parser = argparse.ArgumentParser()
parser.add_argument('-f','--force_crawl', nargs='+', help='use all or company name', required=False)
parser.add_argument('-c','--choose_crawl', nargs='*', help='use all, r for remaining, or company name', required=False)
args=parser.parse_args()

class CrawlPrepare:

    def __init__(self) -> None:
        self.db = DBConnect()
        self.all_job_listings = set([i[0] for i in self.db.sql_fetch_columns(JobListingMeta.url)])

    def get_requested_crawl(self):
        if 'all' in args.choose_crawl:
            print("requested crawl triggered")
            crawl_list=list(self.all_job_listings)

        if 'r' in args.choose_crawl:
            all_crawlable_listings = self.determine_runnable_listings()
            
            return all_crawlable_listings

        if args.choose_crawl and 'all' not in args.choose_crawl and 'r' not in args.choose_crawl:
            args_in_list = args.choose_crawl
            for i in args_in_list:
                if i not in self.all_job_listings:
                    print(i, "is not is current job listing")
                    args_in_list.remove(i)
                crawl_list=args_in_list
            crawl_list = list(crawl_list)

        return crawl_list

    def get_forced_crawl(self):
        if args.force_crawl and 'all' in args.force_crawl:
            print("force crawl triggered")
            crawl_list=self.all_job_listings

        if args.force_crawl and 'all' not in args.force_crawl:
            print("Checking if job listing match")
            for i in args.force_crawl:
                if i not in self.all_job_listings:
                    print(i, "is not is current job listing")
                    args.force_crawl.remove(i)
            crawl_list=args.force_crawl
        crawl_list = list(crawl_list)
        return crawl_list

    def determine_runnable_listings(self):
        column = CrawlLogs.last_attempted_crawl
        utc_now = pytz.utc.localize(datetime.utcnow())
        now = utc_now.astimezone(pytz.timezone("US/Pacific"))
        one_day_ago = now - timedelta(days=1)
        all_listings_crawled_in_last_24_hr = self.db.sql_fetchall_records(CrawlLogs, [{"colname":column, "operator":"le", "value":one_day_ago}])
        non_crawlable_listings = set()

        if all_listings_crawled_in_last_24_hr:
            for i in all_listings_crawled_in_last_24_hr:
                non_crawlable_listings.add(i.get('url'))
        
        crawlable_listings = list(self.all_job_listings - non_crawlable_listings)

        return crawlable_listings


if not args.force_crawl and not args.choose_crawl:
    print("No args provided for force")
    exit()
if args.force_crawl:
    crawl_list = CrawlPrepare().get_forced_crawl()
if args.choose_crawl:
    crawl_list = CrawlPrepare().get_requested_crawl()

AddCronLogs().add_cron_logs({"info":"cron crawl"})

print('crawl list:', crawl_list)
Crawl().start_crawling(crawl_list)
