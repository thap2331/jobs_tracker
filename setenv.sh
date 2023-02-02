#!/bin/bash


if [[ $# -eq 0 ]] ; then
    echo "Prod mode to be activated"
    run_mode='prod'
else
    run_mode=$1
fi



set -o allexport
set -a

# if empty parameter is passed
if [ $run_mode == "test" ]
then
    echo "Test mode activated"
    source .env.dev
else
    echo "Prod mode activated"
    source .env
fi

set +o allexport
set +a
