#!/usr/bin/env sh

if [ ! -d .venv ]; then 
    python3 -m venv .venv
    echo '*' > .venv/.gitignore
fi

git config --local core.hooksPath .githooks/