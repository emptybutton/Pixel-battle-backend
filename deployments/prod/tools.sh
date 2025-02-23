#!/bin/bash

function isHealthy {
    local state=`docker inspect $1 -f {{.State.Health.Status}}`
    echo $state | grep -qF healthy
}

conf=deployments/prod/docker-compose.yaml
