import sys
sys.path.insert(0, '.')
from sqlalchemy import create_engine
from database.data_models import Base

db_path = "jobs.db"
engine = create_engine(f'sqlite:///{db_path}', echo = False)

Base.metadata.create_all(engine)