#!/bin/bash

# Author: Abolfazl
# Version: v1.0.0
# Date: 5/16/25
# Description: entrypoint for PetShop API.
# Usage: ./dev_entrypoint.sh

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
