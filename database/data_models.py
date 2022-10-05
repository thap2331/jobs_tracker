from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

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