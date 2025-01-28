#!/bin/ash

if [ ! -d ".venv" ]; then
    poetry install
fi

poetry run $@
