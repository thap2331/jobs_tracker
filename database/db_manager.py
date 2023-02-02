import sys
sys.path.insert(0, '.')

import os, psycopg2
from sqlalchemy import update, inspect, insert as sqlalchemy_insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from sqlalchemy.dialects.postgresql import insert

from database.db_configs import GetDBCreds
from database.data_models import Jobs

class DBConnect:
    def __init__(self) -> None:
        self.psycopg2_conn_string = GetDBCreds().get_conn_string_python_psycopg2()
        conn_string = GetDBCreds().get_conn_string_sql_alchemy()
        self.engine = create_engine(conn_string)

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

    def sql_fetch_columns(self, colname):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            all_records = session.query(colname).all()
            return all_records
        except Exception as e:
            print(e)
        finally:
            session.close()

    def sql_execute_statement(self, statement, values=None):
        try:
            #replace below with sqlalchemy
            conn = psycopg2.connect(self.psycopg2_conn_string)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            conn.close()
        
    def sql_fetchall_records(self, table, conditions=[]):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            if conditions:
                # loop and add all conditions
                # https://stackoverflow.com/questions/41305129/sqlalchemy-dynamic-filtering
                if not isinstance(conditions[0], dict):
                    print("conditions should be a dict")
                    return

                cond1=conditions[0]
                col=cond1["colname"]
                operator=cond1["operator"]
                value=cond1["value"]
                if operator=="le":
                    all_records = session.query(table).filter(col >= value)
            else:
                all_records = session.query(table).all()
            records = [{c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs} for obj in all_records]
            return records
        except Exception as e:
            print(e)
        finally:
            session.close()

    def sql_fetch_records_with_conditions(self, table):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            all_records = session.query(table).filter(table.last_attempted_crawl <= now)
            records = [{c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs} for obj in all_records]
            return records
        except Exception as e:
            print(e)
        finally:
            session.close()

    def update_records(self, tablename, col_to_update, col_to_update_val, condition_col, condition_col_val):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            session.query(Jobs).filter(Jobs.job_link == condition_col_val).update({col_to_update: col_to_update_val})
            session.commit()
        except Exception as e:
            print(e)
        finally:
            session.close()



class Ingestion:
    def __init__(self) -> None:
        self.conn_string = GetDBCreds().get_conn_string_sql_alchemy()
        self.db = DBConnect()
        self.engine = create_engine(self.conn_string)
    
    def ingest_data(self, data):
        if isinstance(data, list):
            for record in data:
                self.db.insert(record)
                print('insertion attempt: ', record)
            print(f'{len(data)} records inserted.')
            return

        self.db.insert(data)

        return

    def insert_using_engine(self, table, data):
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    sqlalchemy_insert(table),
                    data
                    )
        except Exception as e:
            print(e)

    def insert_data(self, table, data):
        dict_or_list = any([isinstance(data, dict), isinstance(data, list)])
        
        if dict_or_list is False:
            print(f"Data ({data}) is neither a dict nor a list.")
            return
        
        #If data is a list
        are_dict = True
        if isinstance(data, list):
            #all inside should be a dict
            are_dict = all([isinstance(i, dict) for i in data])

        if not are_dict:
            print(f"All data inside a list ({data}) are not a dict.")
            return

        #If data is a dict
        if isinstance(data, dict):
            data = [data]

        try:
            with self.engine.connect() as conn:
                conn.execute(
                    sqlalchemy_insert(table),
                    data
                    )
        except Exception as e:
            print(e)
        
        return