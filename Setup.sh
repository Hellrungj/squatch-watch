#!/bin/bash

#Create Log Files
DIR=$PWD/logs/temp/
[ ! -d "$DIR" ] && mkdir -p "$DIR"

# install python
# apt-get install python3

# Setup pipenv
# apt-get install pipenv

# Setup Env
# pipenv shell

# Install Dependencies
# pipenv install
 
# Mirgates the Database
# python manage.py mirgate

# Create Superuser
# python manage.py superuser

# Run Server
# python manage.py runserver