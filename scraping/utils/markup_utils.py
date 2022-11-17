import sys
sys.path.insert(0, '.')

from requests_html import HTMLSession
import requests

class MarkupUtils:

    def normal_requests(self, url : str):
        markup = ''
        try:
            response = requests.get(url, timeout=2)
            markup = response.text
        except requests.exceptions.Timeout as e:
            return e

        return markup

    def render_request_html(self, url):
        session = HTMLSession()
        response = session.get(url)
        response.html.render()
        rendered_html = response.html
        session.close()

        return rendered_html

