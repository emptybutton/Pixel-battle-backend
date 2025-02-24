#!/bin/ash

while true; do
    ash refresh-ssl.sh
    sleep `shuf -i 0-29 -n 1`d
done
