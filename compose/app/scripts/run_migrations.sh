#!/bin/bash
pipenv run python /code/manage.py makemigrations &&
pipenv run python /code/manage.py migrate