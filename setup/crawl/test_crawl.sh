#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "No argument provided. Please provide dup or up"
    exit
fi

if [[ $1 == "dup" ]]; then
    # Fresh crawl with compose down and up
    docker compose down
    docker compose up database_test test_entrypoint -d

    docker exec test_box bash -c "python scraping/crawl.py -c r"
    docker compose down

elif [[ $1 == "up" ]]; then
    docker compose up database_test test_entrypoint -d
    docker exec test_box bash -c "python scraping/crawl.py -c r"

elif [[ $1 == "jr" ]]; then
    docker exec test_box bash -c "python scraping/crawl.py -c r"

elif [[ $1 == "dtup" ]]; then
    docker compose up database_test test_entrypoint -d
fi