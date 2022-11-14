import sys
sys.path.insert(0, '.')

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from validator_collection import validators
import requests, inspect, importlib

from scraping.pipeline import ProcessData
from database.data_models import Jobs
from database.db_manager import DBConnect
from database.data_models import JobListingMeta
from sqlalchemy import select
from scraping.title_base import TitleStrategies
from scraping.utils.url_utils import UrlUtils


class StrategyList():

    def __init__(self) -> None:
        self.strategies = self.load_strategies()

    def get_strategy_from_setting(self, db_settings) -> TitleStrategies:
        for strategy in self.load_strategies():
            # print(f'Trying {strategy.__class__.__name__}')
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
        pass

    def get_soup(self, url : str):

        markup = requests.get(url)
        soup = BeautifulSoup(markup.content, features='lxml')

        return soup

    def get_all_links(self, soup, url):
        proper_links = []
        all_links_tags = soup.find_all('a')
        all_links = [i.get('href') for i in all_links_tags]

        for link in all_links:
            #join url
            url = urljoin(url, link)

            #check for should follow
            if UrlUtils().should_follow(url):
                proper_links.append(url)

        return proper_links


class TitleFinderStrategy:

    def __init__(self) -> None:
        pass

    def strategy_from_settings(self, config):
        strategy_from_settings = StrategyList().get_strategy_from_setting(config)
        if strategy_from_settings:
            return strategy_from_settings

        return False

    def strategy_finder(self, config):
        strategies_list = StrategyList().load_strategies()

        listing_url = config.get('url')
        title = config.get('job_title')
        soup = ScrapeUtils().get_soup(listing_url)
        all_urls = ScrapeUtils().get_all_links(soup=soup, url=listing_url)

        if all_urls:
            print('\nTesting ', len(all_urls), 'for ', listing_url, 'Trying different strategies.\n')

        #try in order
        for url in all_urls:
            markup = ScrapeUtils().get_soup(url)
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
                

class CrawlPrepare:

    def __init__(self) -> None:
        self.db = DBConnect()
        self.data = self.db.sql_fetchall_records(JobListingMeta)
        self.title_finder = TitleFinderStrategy()

    def find_title_using_existing_settings(self, data):
        all_urls = []
        found_title = False
        stratgey_in_settings = self.title_finder.strategy_from_settings(data)
        if stratgey_in_settings:
            listing_url = data.get('url')
            title = data.get('job_title')
            soup = ScrapeUtils().get_soup(listing_url)
            all_urls = ScrapeUtils().get_all_links(soup=soup, url=listing_url)

        if all_urls:
            print('\nTesting ', len(all_urls), 'for ', listing_url, 'Setting found in existing settings.\n')

        for url in all_urls:
            markup = ScrapeUtils().get_soup(url)
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


    def go_over_all_listings(self):
        for data in self.data:
            stratgey_in_settings = self.title_finder.strategy_from_settings(data)
            if stratgey_in_settings:
                self.find_title_using_existing_settings(data)
                continue

            self.title_finder.strategy_finder(data)

CrawlPrepare().go_over_all_listings()
