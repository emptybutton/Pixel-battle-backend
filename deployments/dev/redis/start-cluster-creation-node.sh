#!/bin/ash

ash /mnt/start-node.sh & ash /mnt/create-cluster-if-not-exists.sh
tail -f /dev/null
