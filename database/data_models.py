from sqlalchemy import Column, String, Integer, ForeignKey, Identity, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Jobs(Base):

    __tablename__ = "jobs"
    id = Column(String, primary_key=True)
    job_link = Column(String)
    job_title = Column(String)

    def __init__(self, id, job_link, job_title):
        self.id = id
        self.job_link = job_link
        self.job_title = job_title


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

    def __init__(self, url, title_in_link, title_in_posting, title_in_page_title, job_link_pattern, job_title,
    company_name, company_website, alternative_names, source_type):
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


class CrawlLogs(Base):

    __tablename__ = 'crawlogs'
    url = Column(String, primary_key = True)