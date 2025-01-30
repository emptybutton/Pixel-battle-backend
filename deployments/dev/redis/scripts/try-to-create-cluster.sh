#!/bin/ash

delay_seconds=1


sleep $delay_seconds

while ! ash /mnt/scripts/is-cluster-ok.sh; do
     redis-cli \
     --cluster create redis1:6379 redis2:6379 redis3:6379 \
     --cluster-yes

     sleep $delay_seconds
done
