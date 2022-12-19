# Advent of Code 2022 solutions of each day

## Requirements
* Python 3.11
* Poetry 1.3
* Django 4.1.4

## Installing Python
https://www.python.org/downloads/release/python-3111/

## Installing Poetry
https://python-poetry.org/docs/#installation

# Setup database
To use default setup `SQLite` just run `poetry run python manage.py migrate`. It will setup you up with a fresh SQLite database, that will be used in solutions. If you wish to setup some other database solution, then be sure to checkout https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Setup caching
Since we have database in place and we don't really care about performance in this case, we going to use Database caching provided by Django. To setup cache table in your database, just run `poetry run python manage.py createcachetable`.  
**NB!** As `Advent of Code` creator, **Eric Wastl**, mentioned, the requests for receiving input for your problems is costly, so it is better to cache them if possible.

## Running project with Poetry
To start the application `poetry run python manage.py runserver`.

Once application is running you can access it at `http://localhost:8000/`. Once application is running, you can access year route with list of different days, that have solutions. On solution page you will be able to either upload your input file or provide URL to it.

Input data is persistent(usually, depends on problem and input data), so once you uploaded your input solution will calculate result based on it, and you don't need to upload it again (even though, you can).