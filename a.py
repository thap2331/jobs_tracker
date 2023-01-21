from database.db_configs import GetDBCreds
import os

# print(os.getenv("emailId"))
# print(os.getenv("run_mode"))

print(GetDBCreds().get_creds_json())

print(GetDBCreds().get_psql_conn_string_sql_alchemy())
