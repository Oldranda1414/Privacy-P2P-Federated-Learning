#!/usr/bin/env bash

DIR="src/.venv"

if [ -d "$DIR" ]; then
    rm -rf "$DIR"
fi
