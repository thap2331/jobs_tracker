import os

class GetDBCreds:
    def __init__(self):
        self.run_mode = self.get_runmode()

        #Actually extract from compose if you can
        self.prod_host_name             = "jt_pg_container"
        self.prod_db_name               = "jt_db" 
        self.prod_port_exposed          = 5432
        self.test_host_name             = "test_jt_pg_container"
        self.test_db_name               = "test_jt_db"
        self.test_port_exposed          = 5432
        self.test_port_exposed_to_host  = 5433

    def get_runmode(self):
        my_run_mode = None

        if os.getenv("run_mode")=="prod" or os.getenv("run_mode") is None:
            my_run_mode = "prod"
        
        if os.getenv("run_mode") in ["dev", "test"]:
            my_run_mode = "test"

        return my_run_mode

    def get_creds_json(self):
        if self.run_mode == "prod":
            prod_db_creds = {
                "host":self.prod_db_name,
                "user":"postgres",
                "password":"pass",
                "db_name":self.prod_db_name,
                "port":self.prod_port_exposed
            }
            return prod_db_creds

        if self.run_mode == "test":
            test_db_creds = {
                "host":self.test_db_name,
                "user":"postgres",
                "password":"pass",
                "db_name":self.test_db_name,
                "port":self.test_port_exposed
            }
            return test_db_creds

    def get_conn_string_sql_alchemy(self):
        if self.run_mode == "prod":
            connection_string=f'postgresql+psycopg2://postgres:pass@{self.prod_host_name}:{self.prod_port_exposed}/{self.prod_db_name}'

        if self.run_mode == "test":
            connection_string=f'postgresql+psycopg2://postgres:pass@{self.test_host_name}:{self.test_port_exposed}/{self.test_db_name}'

        return connection_string 

    def get_conn_string_python_psycopg2(self):
        if self.run_mode == "prod":
            connection_string = f'host={self.prod_host_name}\
                                    dbname={self.prod_db_name}\
                                    user=postgres\
                                    password=pass\
                                    port={self.prod_port_exposed}'

        if self.run_mode == "test":
            connection_string = f'host={self.test_host_name}\
                                    dbname={self.test_db_name}\
                                    user=postgres\
                                    password=pass\
                                    port={self.test_port_exposed}'
        return connection_string