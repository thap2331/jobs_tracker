import sys
sys.path.insert(0, '.')

from requests_html import HTMLSession
import requests, time

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
        rendered_html = response.html.html
        session.close()

        return rendered_html

    def render_using_selenium(self, url):
        # Selenium 4 for loading the Browser Driver 
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        # Web Driver Manager
        from webdriver_manager.chrome import ChromeDriverManager

        # Initialising the Chrome Driver
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        # Delay to load the contents of the HTML FIle
        time.sleep(2)
        page_source = driver.page_source

        return page_source
