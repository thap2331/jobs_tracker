import sys
sys.path.insert(0, '.')

from bs4 import BeautifulSoup
from validator_collection import validators
import requests, inspect, importlib

from scraping.pipeline import ProcessData
from database.data_models import Jobs
from database.db_manager import DBConnect
from database.data_models import JobListingMeta
from sqlalchemy import select
from scraping.title_base import TitleStrategies
from scraping.utils.url_utils import UrlUtils
from scraping.utils.extract_links import ExtractAllLinks
from scraping.utils.markup_utils import MarkupUtils


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

    def extract_links(self, link, render=False):
        all_urls = []
        if render:
            markup = self.markup_utils.render_request_html(link)
        else:
            markup = self.markup_utils.normal_requests(link)

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
        all_urls = self.scrapeutils.extract_links(listing_url)

        if all_urls:
            print('\nTesting ', len(all_urls), 'for ', listing_url, 'Trying different strategies.\n')

        #try in order
        for n, url in enumerate(all_urls):
            markup = MarkupUtils().normal_requests(url)
            if 'timeout' in str(markup).lower():
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
                    print('\n job data from different strategy:', job.__dict__)
                    ProcessData().process_data([job])
                    break
            sys.stdout.write(f'\r{n} of {len(all_urls)} completed.')
            sys.stdout.flush()


class CrawlPrepare:

    def __init__(self) -> None:
        self.db = DBConnect()
        self.data = self.db.sql_fetchall_records(JobListingMeta)
        self.title_finder = TitleFinderStrategy()
        self.scrapeutils = ScrapeUtils()

    def find_title_using_existing_settings(self, data):
        all_urls = []
        found_title = False
        stratgey_in_settings = self.title_finder.strategy_from_settings(data)
        if stratgey_in_settings:
            listing_url = data.get('url')
            title = data.get('job_title')
            all_urls = self.scrapeutils.extract_links(listing_url)

        if all_urls:
            print('\nTesting ', len(all_urls), 'for ', listing_url, 'Setting found in existing settings:',
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
                print('\n job data found from existing settings', job.__dict__)
            sys.stdout.write(f'\r{n} of {len(all_urls)} completed.')
            sys.stdout.flush()


    def go_over_all_listings(self):
        for data in self.data:
            stratgey_in_settings = self.title_finder.strategy_from_settings(data)
            if stratgey_in_settings:
                self.find_title_using_existing_settings(data)
                continue

            self.title_finder.strategy_finder(data)

CrawlPrepare().go_over_all_listings()
