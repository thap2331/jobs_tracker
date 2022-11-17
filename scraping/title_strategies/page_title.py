from ..title_base import TitleStrategies
from bs4 import BeautifulSoup

class PageTitleAnalyzer(TitleStrategies):

    source = 'title_in_page_title'
    priority = 2

    def db_setting(self, setting):
        title_in_page_title = setting.get('title_in_page_title')
        if title_in_page_title: 
            return True

        return False

    def contains_title(self, title, url, markup):
        titles = title.split(';')
        page_title = BeautifulSoup(markup, features='lxml').title
        if not page_title:
            return False

        page_title=page_title.text.lower()

        if len(titles)>1:
            for title in titles:
                if title in page_title:
                    res = {'title':title}
                    return res

        if title in page_title:
            res = {'title':title}
            return res

        return False