import sys
sys.path.insert(0, '.')

from scraping.pipeline import Ingestion
from database.data_models import CrawlLogs
from datetime import datetime


timenow=datetime.now()
data = CrawlLogs(url="url.com", last_attempted_crawl=timenow)
Ingestion().ingest_data(data)
