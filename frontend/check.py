import psycopg2, json
from psycopg2.extras import RealDictCursor

conn_string='host=test_jt_pg_container dbname=test_jt_db user=postgres password=pass port=5432'
conn = psycopg2.connect(conn_string)
# cursor = conn.cursor()
cursor = conn.cursor(cursor_factory=RealDictCursor)

cursor.execute('SELECT * FROM joblisting')
searchTableData = cursor.fetchall()
print(type(json.dumps(searchTableData)))

cursor.execute('SELECT * FROM jobs')
resultsTableData = cursor.fetchall()
print(json.dumps(resultsTableData))