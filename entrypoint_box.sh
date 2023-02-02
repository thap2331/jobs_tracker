#!/bin/bash

find_entrypoint () {
    if [[ $run_mode == "test" ]]; then 
        entry_container="test_entrypoint"
    elif [[ $run_mode == "dev" ]]; then
        entry_container="test_entrypoint"
    else
        entry_container="prod_entrypoint"
    fi
}
find_entrypoint
# echo "$entry_container"


set -o allexport
set -a

export entry_container="$entry_container"

set +o allexport
set +a