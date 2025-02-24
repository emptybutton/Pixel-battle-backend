#!/bin/bash

source deployments/prod/tools.sh

if [[ "$1" != "-y" && "$1" != "-s" ]]; then
    RED='\033[0;31m'
    CYAN='\033[0;36m'
    NC='\033[0m'

    echo -e "This script may call \`${RED}reset --hard${NC}\` (EVEN ON CTRL+C)."
    echo -e "To don't call \`${RED}reset --hard${NC}\`, use ${CYAN}-s${NC}."
    echo -e "To call without this message use ${CYAN}-y${NC}."
    echo ""
    printf "continue? [y/N] "
    read
    input=$REPLY

    if [[ $input != "y" ]]; then
        exit 0
    fi
fi


function redeploy() {
    docker compose -f $conf stop
    docker compose -f $conf rm -f
    docker compose -f $conf up -d --build --wait
}

if echo $@ | grep -q -e "-s"; then
    redeploy
    exit
fi

isRedeploySuccess=true

until redeploy; do
    git reset --hard HEAD~1
    isRedeploySuccess=false
done

$isRedeploySuccess
