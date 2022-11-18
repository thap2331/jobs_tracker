import sys
sys.path.insert(0, '.')

from database.data_models import Jobs
from database.db_manager import DBConnect


class Validation:
    def __init__(self) -> None:
        self.db = DBConnect()
        self.ingestion = Ingestion()

    def new_found_jobs(self, data, db_records, colname):
        new_jobs = []

        for record in data:
            key_to_compare_against = record.__dict__.get(colname)
            if key_to_compare_against not in db_records:
                new_jobs.append(record)
        
        return new_jobs

    def validate_new_jobs(self, data, table, primary_key=None):
        db_records = self.db.sql_fetchall_columns_records(table=table, colname=primary_key)
        pk_records = [row[0] for row in db_records]
        new_jobs = self.new_found_jobs(data, pk_records, primary_key)

        return new_jobs



class Ingestion:
    def __init__(self) -> None:
        self.db = DBConnect()

    def ingest_data(self, data):
        if isinstance(data, list):
            for record in data:
                self.db.insert(record)
                print('insertion attempt: ', record)
            print(f'{len(data)} records inserted.')
            return

        self.db.insert(data)
        print(f'1 record {data} inserted.')

        return



class ProcessData:
    def __init__(self) -> None:
        self.ingestion = Ingestion()
        self.validation = Validation()

    def process_data(self, data: Jobs):
        validated_data = self.validation.validate_new_jobs(data, Jobs, primary_key='job_link')
        self.ingestion.ingest_data(validated_data)

        return