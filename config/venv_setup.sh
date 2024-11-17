#!/bin/bash

python3 -m venv API_env

source API_env/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

echo "Virtual environment and dependencies setup complete"