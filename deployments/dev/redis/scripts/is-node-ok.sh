#!/bin/ash

echo PING | redis-cli | grep -qF PONG
