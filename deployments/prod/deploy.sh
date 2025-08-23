#!/bin/bash

timeout=900 # 15m
conf=deployments/prod/docker-compose.yaml

docker compose -f $conf down
docker compose -f $conf build

docker compose -f $conf up redis1 redis2 redis3 -d --wait --wait-timeout $timeout
docker exec pixel-battle-redis1 ash /mnt/scripts/create-cluster.sh

docker compose -f $conf up -d --wait-timeout $timeout
