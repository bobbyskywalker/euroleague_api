#!/bin/bash

python3 -m venv API_env

source API_env/bin/activate

pip3 install -r requirements.txt

echo "Virtual environment and dependencies setup complete"