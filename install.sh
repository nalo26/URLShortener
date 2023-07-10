#!/bin/bash

echo "Creating application"

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Please edit .env file and run this script again"
    exit 1
fi

if [ -d .venv]; then
    rm -rf .venv
fi

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

./create_database.sh

