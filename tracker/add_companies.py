import sys
sys.path.insert(0, '.')

import random

from database.db_manager import Ingestion
from database.data_models import JobListingMeta

class AddCompaniesMetadata:

    def __init__(self) -> None:
        self.ingestion = Ingestion()

    def add_company(self, website_link, company_name=None, alternative_names=None):
        if not website_link:
            raise AssertionError('Website link not provided')

        company_name = company_name if company_name else ''
        alternative_names = alternative_names if alternative_names else ''

        id = random.randint(0, 200000)


    def add_job_listing(self, url, job_identifier='link', type='company', company_id=None):
        if type != 'company':
            company_id = 'new_company'


class AddJobListing:

    def __init__(self) -> None:
        self.ingestion = Ingestion()

    def normalize_data(self, **kwargs):
        url = kwargs.get("url")
        title_in_link = kwargs.get("title_in_link")
        title_in_page_title = kwargs.get("title_in_page_title")
        job_link_pattern = kwargs.get("job_link_pattern")
        job_title = kwargs.get('job_title')
        company_name = kwargs.get("company_name")
        company_website = kwargs.get("company_website")
        alternative_names = kwargs.get("alternative_names")
        source_type = kwargs.get("source_type")


        if not url:
            raise ValueError('Url not provided.')

        title_in_posting = False

        # if title_in_link:
        #     if title_in_link.lower() in ['y', 'yes', True]:
        #         title_in_link = True
        #     else:
        #         title_in_link = False

        if not title_in_link:
            title_in_posting = True

        if not job_title:
            raise ValueError("No job title provided.")

        job_title = ';'.join(job_title)

        JobMetaObject = JobListingMeta(
            url=url, 
            title_in_link=title_in_link,
            title_in_posting=title_in_posting, 
            title_in_page_title=title_in_page_title,
            job_link_pattern=job_link_pattern,
            job_title=job_title,
            company_name=company_name,
            company_website=company_website,
            alternative_names=alternative_names,
            source_type=source_type
            )

        return JobMetaObject

    def validate_job_listing(self, joblisting_object):
        print('Trying to validate job listing.')

        if type(joblisting_object) != JobListingMeta:
            return 'Data is not a joblisting object.'



    def add_job_listing(self, job_listing_object):
        print('Trying to add job listing')

        self.ingestion.ingest_data(job_listing_object)
        


# AddCompaniesMetadata().add_company('https://jobs.lever.co/economicmodeling/', 'b', 'emsi')