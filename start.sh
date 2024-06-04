#!/bin/bash

echo "Running migrations"
py manage.py makemigrations

echo "Migrate"
py manage.py migrate

echo "Running server"
py manage.py runserver 0.0.0.0:8000
