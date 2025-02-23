#!/bin/bash

source deployments/prod/tools.sh

docker compose -f $conf create
docker compose -f $conf start redis1 redis2 redis3

until (
    isHealthy pixel-battle-redis1 \
    && isHealthy pixel-battle-redis2 \
    && isHealthy pixel-battle-redis3
); do
    sleep 0.1;
done

docker exec pixel-battle-redis1 ash /mnt/scripts/create-cluster.sh
docker compose -f $conf up -d --wait
