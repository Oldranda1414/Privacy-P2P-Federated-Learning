#!/usr/bin/env bash

# Get the directory where the script is located
TEMP=$(realpath "$0") 
SCRIPT_PATH=$(dirname "$TEMP")

$SCRIPT_PATH/update_graphs.sh

