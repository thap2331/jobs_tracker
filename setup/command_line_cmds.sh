#Prod psql
PGPASSWORD=pass psql -U postgres -h localhost -d jt_db -c '\l'
PGPASSWORD=pass psql -U postgres -h localhost -d jt_db -c 'select * from joblisting'


#Test psql
PGPASSWORD=pass psql -U postgres -h localhost -p 5433 -d test_jt_db -c '\l'
PGPASSWORD=pass psql -U postgres -h localhost -p 5433 -d test_jt_db -c '\d'
PGPASSWORD=pass psql -U postgres -h localhost -p 5433 -d test_jt_db -c 'select * from joblisting'
PGPASSWORD=pass psql -U postgres -h localhost -p 5433 -d test_jt_db -c 'select * from jobs'