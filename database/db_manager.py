from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from database.db_configs import db_path
from sqlalchemy import inspect

class DBConnect:
    def __init__(self) -> None:
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{self.db_path}', echo = True)

    def insert(self, data):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            session.add(data)
        except Exception as e:
            print(e)
        finally:
            session.commit()
            session.close()

    def sql_fetchall_columns_records(self, table, colname):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            records = session.query(table.job_link).all()
            return records
        except Exception as e:
            print(e)
        finally:
            session.close()

    def sql_fetchall_records(self, table):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            all_records = session.query(table).all()
            records = [{c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs} for obj in all_records]
            return records
        except Exception as e:
            print(e)
        finally:
            session.close()


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

        return
