#!/bin/bash
set -e

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo ".venv already exists. Skipping creation."
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "\nPython virtual environment is ready!"
echo "To activate it in the future, run: source .venv/bin/activate" 