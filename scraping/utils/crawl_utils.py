import sys
sys.path.insert(0, '.')

import inspect, importlib, pytz
from datetime import datetime

from scraping.pipeline import ProcessData
from database.data_models import Jobs, CrawlLogs, JobListingMeta
from database.db_manager import DBConnect, Ingestion
from scraping.title_base import TitleStrategies
from scraping.utils.extract_links import ExtractAllLinks
from scraping.utils.markup_utils import MarkupUtils
from scraping.utils.utils import PrepCrawlogs

class StrategyList():

    def __init__(self) -> None:
        self.strategies = self.load_strategies()

    def get_strategy_from_setting(self, db_settings) -> TitleStrategies:
        for strategy in self.load_strategies():
            working_strategy = strategy.db_setting(db_settings)

            if working_strategy:
                return strategy

        return False

    def load_strategies(self):
        all_strategies = []
        for name, cls in inspect.getmembers(importlib.import_module("scraping"), inspect.isclass):
            if issubclass(cls, TitleStrategies):
                all_strategies.append(cls())
        all_strategies_by_priority = sorted(all_strategies, key=lambda x: x.priority)

        return all_strategies_by_priority


class ScrapeUtils:

    def __init__(self) -> None:
        self.extract_links_method = ExtractAllLinks()
        self.markup_utils = MarkupUtils()

    def extract_links(self, link, config):
        all_urls = []
        render = config.get('render')
        if not render:
            markup = self.markup_utils.normal_requests(link)
            all_urls = self.extract_links_method.extract_links_from_markup(markup, domain_url=link)

        #condition1: If normal link extract cannot extract link
        #condition2: if explicit render is asked
        #Even request html cannot extract links, then fallback to selenium render
        if not all_urls or render:
            try:
                markup = self.markup_utils.render_request_html(link)
                all_urls = self.extract_links_method.extract_links_from_markup(markup, domain_url=link)
            except Exception as e:
                print("Error for request html: ",e)
            if not all_urls:
                print("Falling back to selenium render")
                markup = self.markup_utils.render_using_selenium(link)
                all_urls = self.extract_links_method.extract_links_from_markup(markup, domain_url=link)

        return all_urls



class TitleFinderStrategy:

    def __init__(self) -> None:
        self.scrapeutils = ScrapeUtils()

    def strategy_from_settings(self, config):
        strategy_from_settings = StrategyList().get_strategy_from_setting(config)
        if strategy_from_settings:
            return strategy_from_settings

        return False

    def strategy_finder(self, config):
        strategies_list = StrategyList().load_strategies()

        listing_url = config.get('url')
        title = config.get('job_title')
        all_urls = self.scrapeutils.extract_links(listing_url, config)

        if all_urls:
            print('\n\nTesting', len(all_urls), 'urls for', listing_url, 'Trying different strategies.\n')

        #try in order
        for n, url in enumerate(all_urls):
            markup = MarkupUtils().normal_requests(url)
            if 'timeout' in str(markup).lower():
                #make this better. timeout python error only
                continue
            for strategy in strategies_list:
                found_title = strategy.contains_title(title, url, markup)
                if found_title:
                    job_title = found_title.get('title')
                    job = Jobs(
                        job_link=url,
                        job_title=job_title,
                        job_listing_url=listing_url,
                        source=strategy.source
                    )
                    print(f'\n{job_title} job:', job.__dict__.get('job_link'))
                    ProcessData().process_data([job])
                    break
            sys.stdout.write(f'\r{n+1} of {len(all_urls)} completed.')
            sys.stdout.flush()
    
class Crawl:

    def __init__(self) -> None:
        self.db = DBConnect()
        self.all_data = self.db.sql_fetchall_records(JobListingMeta)
        self.title_finder = TitleFinderStrategy()
        self.scrapeutils = ScrapeUtils()
        self.ingestion = Ingestion()

    def find_title_using_existing_settings(self, data):
        all_urls = []
        found_title = False
        stratgey_in_settings = self.title_finder.strategy_from_settings(data)
        if stratgey_in_settings:
            listing_url = data.get('url')
            title = data.get('job_title')
            all_urls = self.scrapeutils.extract_links(listing_url, data)

        if all_urls:
            print('\n\nTesting ', len(all_urls), 'for ', listing_url, 'Setting found in existing settings:',
            stratgey_in_settings.__class__.__name__, '\n')

        for n,url in enumerate(all_urls):
            markup = MarkupUtils().normal_requests(url)
            found_title = stratgey_in_settings.contains_title(title, url, markup)

            if found_title:
                job_title = found_title.get('title')
                job = Jobs(
                    job_link=url,
                    job_title=job_title,
                    job_listing_url=listing_url,
                    source=stratgey_in_settings.source
                )
                ProcessData().process_data([job])
                print(f'\n{job_title} job:', job.__dict__.get('job_link'))
            sys.stdout.write(f'\r{n+1} of {len(all_urls)} completed.')
            sys.stdout.flush()


    def go_over_all_listings(self):
        for data in self.all_data:
            stratgey_in_settings = self.title_finder.strategy_from_settings(data)
            if stratgey_in_settings:
                self.find_title_using_existing_settings(data)
                continue

            self.title_finder.strategy_finder(data)

    def start_crawling(self, crawl_data_list):
        if not crawl_data_list:
            print("No crawl list provided")
            exit()
        crawlable_list = []
        for data_dict in self.all_data:
            if data_dict.get("url") in crawl_data_list:
                crawlable_list.append(data_dict)
        
        print("\nCrawable list: ", crawlable_list, '\n')
        for data in crawlable_list:

            #Add to crawl Logs           
            updated_crawlogs = PrepCrawlogs().prepare_crawlogs_from_last_crawled(data)
            self.ingestion.insert_data(CrawlLogs, updated_crawlogs)

            #Find strategy
            stratgey_in_settings = self.title_finder.strategy_from_settings(data)
            if stratgey_in_settings:
                self.find_title_using_existing_settings(data)
                continue

            self.title_finder.strategy_finder(data)
