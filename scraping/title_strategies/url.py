from ..title_base import TitleStrategies

class UrlAnalyzer(TitleStrategies):

    source = 'title_in_link'
    priority = 1

    def db_setting(self, setting):
        title_in_link = setting.get('title_in_link')
        if title_in_link: 
            return True

        return False

    def contains_title(self, title, url: str, markup):
        if not url:
            return False

        url = url.lower()
        res = {}
        titles = title.split(';')

        if len(titles)>1:
            for title in titles:
                if title in str(url):
                    res['title'] = title
                    return res

        if title in str(url):
            res['title'] = title
            return res

        return False
