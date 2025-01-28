#!/bin/ash

sleep 3

if [ ! -e "/data/nodes.conf" ]; then
    redis-cli \
     --cluster create redis1:6379 redis2:6379 redis3:6379 \
     --cluster-yes
fi
