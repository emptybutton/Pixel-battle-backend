#!/bin/ash

ash /mnt/scripts/start-node.sh & ash /mnt/scripts/try-to-create-cluster.sh
tail -f /dev/null
