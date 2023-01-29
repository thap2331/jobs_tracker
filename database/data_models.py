from sqlalchemy import Column, String, Integer, ForeignKey, Identity, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Jobs(Base):
    #Update this class name to JobsResults since this is filled after scraping

    __tablename__ = "jobs"
    job_link        = Column(String, primary_key=True)
    job_title       = Column(String)
    job_listing_url = Column(String)
    source          = Column(String)
    notified        = Column(Boolean)

    def __init__(self, job_link, job_title, job_listing_url, source, notified=False):
        self.job_link           = job_link
        self.job_title          = job_title
        self.job_listing_url    = job_listing_url
        self.source             = source
        self.notified           = notified

class JobListingMeta(Base):

    __tablename__       = "joblisting"
    url                 = Column(String, primary_key=True)
    title_in_link       = Column(Boolean) #Link or webpage, True if Link
    title_in_posting    = Column(Boolean) #True if title_in_link else false
    title_in_page_title = Column(Boolean) #Require if title in Link is False
    job_link_pattern    = Column(String) #which links to follow - default to structured data, job link pattern
    job_title           = Column(String)
    company_name        = Column(String)
    company_website     = Column(String)
    alternative_names   = Column(String)
    source_type         = Column(String) #Company or ats
    render              = Column(Boolean)

    def __init__(self, url, title_in_link, title_in_posting, title_in_page_title, job_link_pattern, job_title,
    company_name, company_website, alternative_names, source_type, render):
        self.url                    = url
        self.title_in_link          = title_in_link
        self.title_in_posting       = title_in_posting
        self.title_in_page_title    = title_in_page_title
        self.job_link_pattern       = job_link_pattern
        self.job_title              = job_title
        self.company_name           = company_name
        self.company_website        = company_website
        self.alternative_names      = alternative_names
        self.source_type            = source_type
        self.render                 = render


class CrawlLogs(Base):

    __tablename__ = 'crawlogs'
    url = Column(String, primary_key = True)
    last_attempted_crawl = Column(DateTime, nullable = False)