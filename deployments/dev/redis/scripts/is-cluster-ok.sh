#!/bin/ash

echo "CLUSTER INFO" | redis-cli | grep -qF cluster_state:ok
