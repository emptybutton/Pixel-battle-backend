#!/bin/ash

redis-cli --cluster create redis1:6379 redis2:6379 redis3:6379 redis4:6379 --cluster-yes
