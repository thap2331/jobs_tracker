import sys
sys.path.insert(0, '.')

from scraping.utils.utils import ScrapingUtils
import unittest

class TestScrapingUtils(unittest.TestCase):

    def test_title_util(self):
        scraping_utils = ScrapingUtils()
        titles = scraping_utils.title_splitter('data engineer; devops engineer')
        expected_titles = ['data engineer',  'devops engineer', 'data-engineer', 'devops-engineer']
        sorted_titles, sorted_expected_titles = sorted(titles), sorted(expected_titles)

        self.assertEqual(sorted_titles, sorted_expected_titles)

    def test_title_util_with_list(self):
        scraping_utils = ScrapingUtils()
        titles = scraping_utils.title_splitter(['data engineer'])
        expected_titles = []

        self.assertEqual(titles, expected_titles)

if __name__ == '__main__':
    unittest.main()