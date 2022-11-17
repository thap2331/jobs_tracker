from urllib.parse import urljoin
from w3lib.url import canonicalize_url
from furl import furl

class UrlUtils:

    def __init__(self) -> None:
        self.bad_prefix_extension_pattern = {
            'bad_prefixes' : [
                'mail:', 'mailto:', 'matilto:', 'mauilto:', 'maito:', 'mailo:', 'email:', 'emailto:', 'javascript', 'javascrpt', 
                'javscript', 'tel:', 'telefon:', '#', 'void', 'weixin', 'tel.:', 'callto:', 'sms:', 'fax:', 'x-serviceportal', 'video:', 
                'waze:'],

            'bad_extensions' : [
                '.ashx', '.dmg', '.doc', '.docx', '.exe', '.gif', '.jpeg', '.jpg', '.mp4', '.mp3', '.pdf', '.png', 
                '.pptx', '.sh', '.xls', '.xlsx', '.zip', '.dwg', '/login', '/signup'
            ],

            'bad_patterns' : [
                '^/events/', '^/blog/', '^/news/', '^/account/', '^/user/', '^/resumes/', '^/news--events/', 
                '^/users/', '^/press/download/', '^/pdf/']
        }

    def should_follow(self, link: str):
        bad_extensions = self.bad_prefix_extension_pattern.get('bad_extensions')
        bad_prefixes = self.bad_prefix_extension_pattern.get('bad_prefixes')

        for bad_prefix in bad_prefixes:
            if link.startswith(bad_prefix):
                return False

        for bad_ending in bad_extensions:
            if link.endswith(bad_ending):
                return False

        return True

    def clean_links(self, all_links, domain_url):
        proper_links = []

        for link in all_links:
            if not link:
                continue
            url = urljoin(domain_url, link)


            #check for should follow
            if self.should_follow(url):
                #normalize url before adding
                proper_links.append(url)

        proper_links = list(set(proper_links))

        return proper_links

    def strip_and_lower_url(self, url: str):
            url = url.lower()
            url = url.strip()
            url = url.strip('/')

            return url

    def sort_url_args(self, url: str):
        if '?' not in url:
            return url
        else:
            return canonicalize_url(url)

    def params_cleaner(self, url: str):
        if '?' not in url:
            return self.strip_and_lower_url(url)

        furled = furl(url)
        for key, values in self.universal_bad_args['kv_match'].items():
            if key in furled.args and furled.args[key] in values:
                furled.remove(key)

        furled.remove(self.universal_bad_args['keys_only'])

        return self.strip_and_lower_url(furled.url)

    def normalize_url_origin(self, url: str):
        #see furl(url).origin
        url = str(url).replace('https://.', 'https://')

        return url

    def path_normalize(self, url: str):
        parsed_url = furl(url)
        parsed_url.scheme = 'https'
        parsed_url.path.normalize()
        normalized_path_url = parsed_url.url

        return normalized_path_url

    def standard_url_cleaner(self, url):
        if not isinstance(url, str):
            return url

        url = self.normalize_url_origin(url)
        url = self.sort_url_args(url)
        url = self.path_normalize(url)
        url = self.params_cleaner(url)

        return url