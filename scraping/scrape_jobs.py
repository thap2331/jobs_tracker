import sys
sys.path.insert(0, '.')

from bs4 import BeautifulSoup
import requests
from scraping.pipeline import ProcessData
import hashlib
from database.data_models import Jobs

url = "https://www.texastribune.org/jobs/"
markup = requests.get(url)
soup = BeautifulSoup(markup.content, features='lxml')

all_links = soup.find_all('a')
job_links = []
jobs_object_list = []

for link in all_links:
    if '/jobs/' in str(link) and 'https' in str(link):
            job_links.append(link['href'])

for link in job_links:
    jobs_object_list.append(
        Jobs(
        id=hashlib.sha1(link.encode()).hexdigest(),
        job_link=link,
        job_title=link.strip("/").split("/")[-1]
        )
    )

proc = ProcessData()
# for job_obj in jobs_object_list:
proc.process_data(jobs_object_list)
    # print(job_obj.__dict__.get('id'), job_obj.__dict__.get('job_link'))