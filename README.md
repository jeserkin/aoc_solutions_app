# Advent of Code 2022 solutions of each day

## Requirements
* Python 3.11
* Poetry 1.3
* Django 4.1.4

## Installing Python
https://www.python.org/downloads/release/python-3111/

## Installing Poetry
https://python-poetry.org/docs/#installation

## Running project with Poetry
To start the application `poetry run python manage.py runserver`.

Once application is running you can access it at `http://localhost:8000/`. Once application is running, you can access year route with list of different days, that have solutions. On solution page you will be able to either upload your input file or provide URL to it.

Input data is persistent(usually, depends on problem and input data), so once you uploaded your input solution will calculate result based on it, and you don't need to upload it again (even though, you can).