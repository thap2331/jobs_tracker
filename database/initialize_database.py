import sys, psycopg2, json
sys.path.insert(0, '.')
from sqlalchemy import create_engine
from database.data_models import Base
from database.db_configs import GetDBCreds

conn_string = GetDBCreds().get_conn_string_sql_alchemy()

engine = create_engine(conn_string)
Base.metadata.create_all(engine)


# prod = GetDBCreds().get_psql_conn_string_sql_alchemy().get("prod")
# test = GetDBCreds().get_psql_conn_string_sql_alchemy().get("test")

# engine = create_engine(test)
# Base.metadata.create_all(engine)

# parser = argparse.ArgumentParser()
# parser.add_argument("-r", "--run_mode", help="run mode")
# args = parser.parse_args()

# if not args.run_mode:
#     print("No run mode provided")
#     exit()

# if args.run_mode == "test":
#     print("ensure that the database is active")
#     # Test database
#     engine = create_engine(db_path)

# if args.run_mode == "prod":
#     print("Prod run mode provided")

#     db_path=f'postgresql+psycopg2://{db_creds["user"]}:{db_creds["password"]}@{db_creds["host"]}/jt_pg_db'
#     engine = create_engine(db_path)

#     Base.metadata.create_all(engine)

