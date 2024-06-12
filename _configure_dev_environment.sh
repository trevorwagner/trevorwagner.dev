#!/usr/bin/env sh

if [ ! -d .venv ]; then python3 -m venv .venv; fi

git config --local core.hooksPath .githooks/