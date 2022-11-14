import sys
sys.path.insert(0, '.')

import argparse
from database.data_models import JobListingMeta
from tracker.add_companies import AddJobListing

parser = argparse.ArgumentParser()
parser.add_argument('--url', '-u', help='Provide a url')
parser.add_argument('--title_in_link', '-t', action='store_true', default=False, help='Is the title in link')
parser.add_argument('--title_in_page_title', '-pt', action='store_true', default=False, help='Title in page title')
parser.add_argument('--job_link_pattern', '-jl', default='', help='Is the title in link')
parser.add_argument('--job_title', '-jt', nargs='+', default='', help='Provide the job title.')
parser.add_argument('--company_name', '-c', default='', help='Company name')
parser.add_argument('--company_website', '-w', default='', help='Company website.')
parser.add_argument('--alternative_names', '-n', default='', help='Alternative names.')
parser.add_argument('--source_type', '-s', default='', help='Source types.')


args = parser.parse_args()
url = args.url
title_in_link = args.title_in_link
title_in_page_title = args.title_in_page_title
job_link_pattern = args.job_link_pattern
job_title = args.job_title
company_name = args.company_name
company_website = args.company_website
alternative_names = args.alternative_names
source_type = args.source_type



normalized_data = AddJobListing().normalize_data(
    url=url,
    title_in_link=title_in_link,
    title_in_page_title=title_in_page_title,
    job_link_pattern=job_link_pattern,
    job_title = job_title,
    company_name=company_name,
    company_website=company_website,
    alternative_names=alternative_names,
    source_type=source_type
)

print(normalized_data.__dict__)
AddJobListing().add_job_listing(normalized_data)

