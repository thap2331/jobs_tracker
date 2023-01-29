import sys
sys.path.insert(0, '.')


from database.db_configs import GetDBCreds
from database.db_manager import DBConnect
from database.data_models import Jobs, CrawlLogs, JobListingMeta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from tracker.add_crawl_logs import AddCrawlLogs
from datetime import datetime, timedelta
import pytz, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c','--choose_crawl', nargs='*', help='use all or company name', required=False)
args=parser.parse_args()

print(args.choose_crawl)



conn_string = GetDBCreds().get_conn_string_sql_alchemy()
engine = create_engine(conn_string)

# AddCrawlLogs().add_crawl_logs({"url":"url.com"})
# AddCrawlLogs().add_test_data()
# table = CrawlLogs
# cond = CrawlLogs.last_attempted_crawl
AddCrawlLogs().add_crawl_logs({"url":"https://www.texastribune.org/jobs/"})

#two days ago
utc_now = pytz.utc.localize(datetime.utcnow())
now = utc_now.astimezone(pytz.timezone("US/Pacific"))
pst_timenow = now - timedelta(days=2)





# print(now, now.tzinfo, one_day_ago)

# DBConnect().sql_fetchall_records(CrawlLogs, [{"colname":cond, "operator":"le", "value":now}])

# a = CrawlLogs.dynamic_filter([('last_attempted_crawl','le',now)]).all()
# print(a)
# try:
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     all_records = session.query(table).filter(cond <= now)
#     records = [{c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs} for obj in all_records]
#     print(records)
# except Exception as e:
#     print('error ',e)
# finally:
#     session.close()