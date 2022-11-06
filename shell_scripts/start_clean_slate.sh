#!/bin/bash

set -e

if [ -e database/jobs.db ]
then
    rm database/jobs.db
else
    echo "No database."
fi


echo "Initializing database"
python database/initialize_database.py