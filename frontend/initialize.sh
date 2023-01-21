#!/bin/bash
set -e


FILE=.env

if [[ -f "$FILE" ]]; then
    echo "$FILE exists."
else
    echo "$FILE does not exists."
    echo "Creating $FILE"
    echo -e "run_mode=prod\nemailId=\nonePasswordEmail=" > $FILE
fi

chmod +x $FILE

python3 database/initialize_database.py