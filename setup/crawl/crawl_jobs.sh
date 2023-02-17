#!/bin/bash

cd $2
source setenv.sh $1

if [[ $# -ne 3 ]]; then
    echo "Three args required. First: run mode, second: path, thrid: run different commands."
    exit
fi

if [[ $3 == "dup" ]]; then
    # Fresh crawl with compose down and up
    docker compose down
    docker compose up $1_database $1_entrypoint -d

    docker exec $1_box bash -c "python scraping/crawl.py -c r"
    docker compose down

elif [[ $3 == "up" ]]; then
    docker compose up test_database test_entrypoint -d
    docker exec test_box bash -c "python scraping/crawl.py -c r"

elif [[ $3 == "jr" ]]; then
    docker exec test_box bash -c "python scraping/crawl.py -c r"

elif [[ $3 == "dtup" ]]; then
    docker compose up test_database test_entrypoint -d
fi