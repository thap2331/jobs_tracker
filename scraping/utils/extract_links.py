import sys
sys.path.insert(0, '.')

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from scraping.utils.url_utils import UrlUtils
from scraping.utils.markup_utils import MarkupUtils


class ExtractAllLinks:

    def __init__(self) -> None:
        self.urlutils = UrlUtils()
        self.markup_utils = MarkupUtils()

    def extract_links_from_markup(self, markup, domain_url):
        if not markup:
            return []

        soup = BeautifulSoup(markup, features='lxml')
        all_links_tags = soup.find_all('a')
        all_links = [i.get('href') for i in all_links_tags]
        proper_urls = self.urlutils.clean_links(all_links, domain_url)

        return proper_urls

    def normal_url_requests(self, url, domain_url):
        markup = self.markup_utils.get_markup_normal_requests(url)
        if not markup:
            return []

        soup = BeautifulSoup(markup, features='lxml')
        all_links_tags = soup.find_all('a')
        all_links = [i.get('href') for i in all_links_tags]
        proper_urls = self.urlutils.clean_links(all_links, domain_url)

        return proper_urls

    def request_html_extract_links():
        pass

    def request_html_render_extract_links():
        pass

    def render_and_grab_all_links(self, url):
        session = HTMLSession()
        markup = session.get(url)
        markup.html.render()
        rendered_links = markup.html.links
        all_links = self.urlutils.clean_links(rendered_links, url)
        session.close()

        return all_links