import sys
sys.path.insert(0, '.')

from bs4 import BeautifulSoup
import requests
from scraping.pipeline import ProcessData
import hashlib
from database.data_models import Jobs

class ScrapeData:

    def __init__(self) -> None:
        pass

    def get_soup(self, url : str):

        markup = requests.get(url)
        soup = BeautifulSoup(markup.content, features='lxml')

        return soup

    def get_all_links(self, soup):
        all_links = soup.find_all('a')

        return all_links

    def parse(self, soup, company_identifier=None):
        if not company_identifier:
            return

        jobs_object_list = []
        if company_identifier == "tt":
            print(company_identifier)
            all_links = soup.find_all('a')
            job_links = []

            for link in all_links:
                if '/jobs/' in str(link) and 'https' in str(link):
                        job_links.append(link['href'])

            for link in job_links:
                if 'sales' in link:
                    jobs_object_list.append(link.strip("/").split("/")[-1])

        elif company_identifier == "onx":
            print(company_identifier)

            # all_job_classes = soup.find_

# col_with_type = {}
# for c in JobListingMeta.__table__.columns:
#     col_with_type[c.key]=c.type
# print('col: ', col_with_type)

# for i in JobMetaObject.__dict__:
#     if i in cols:
#         # print(i, col_with_type.get(i))
#         if not i:
#             print(i)

# if not url:
#     raise ValueError('Url not provided.')

# title_in_posting = True

# if title_in_link:
#     if title_in_link.lower() not in ['y', 'yes']:
#         title_in_link = True
#     else:
#         title_in_link = False

# if title_in_link:
#     title_in_posting = False

# JobMetaObject = JobListingMeta(
#     url=url, 
#     title_in_link=title_in_link,
#     title_in_posting=title_in_posting, 
#     title_in_page_title=title_in_page_title,
#     job_link_pattern=job_link_pattern,
#     company_name=company_name,
#     company_website=company_website,
#     alternative_names=alternative_names,
#     source_type=source_type
#     )

# cols = [c.key for c in JobListingMeta.__table__.columns]

# AddJobListing().validate_job_listing(JobMetaObject)
# AddJobListing().add_job_listing(JobMetaObject)all(attrs={"class" : "careers__listing"})
        #     for i in all_job_classes:
        #         job_title = i.find(attrs={"class":"careers__title"}).text
        #         if "senior product designer" in job_title.lower():
        #             link=i.find('a').get('href')
        #             jobs_object_list.append(job_title)
        # print(jobs_object_list)

scrape = ScrapeData()
url_dict = {"tt":"https://www.texastribune.org/jobs/", "onx":"https://www.onxmaps.com/join-our-team"}
for key in url_dict.keys():
    soup = scrape.get_soup(url_dict[key])
    scrape.parse(soup, key)
