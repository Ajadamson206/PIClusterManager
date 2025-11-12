#!/usr/bin/env bash

# The daemon does NOT need to run this script, it should run cluster-manager.py directly
# This script is only for users who want to manually start the cluster manager
set -e

venv_name=".venv"

# Check if the virtual environment exists
if [ ! -d "$venv_name" ]; then
    echo "Required Libraries are not installed. Run INSTALL.sh first."
    exit 1
fi

# Activate the virtual environment
source "$venv_name/bin/activate"

# Start the cluster manager
python3 src/cluster-manager.py