# Advent of Code 2022- solutions

## Requirements
* Python 3.11
* Poetry 1.3
* Django 4.1.4
* Django-ninja 0.20.0

## Installing Python
https://www.python.org/downloads/release/python-3111/

## Installing Poetry
https://python-poetry.org/docs/#installation

# Setup database
To use default setup `SQLite` just run `poetry run python manage.py migrate`. It will setup you up with a fresh SQLite database, that might be used in solutions. If you wish to setup some other database solution, then be sure to checkout https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Setup caching
Since we have database in place and we don't really care about performance in this case, we might use Database caching provided by Django. To setup cache table in your database, just run `poetry run python manage.py createcachetable`.  
**NB!** As `Advent of Code` creator, **Eric Wastl**, mentioned, the requests for receiving input for your problems is costly, so it is better to cache them if possible.

## Running project with Poetry
To start the application `poetry run python manage.py runserver`.

Once application is running you can access API at `http://localhost:8000/api/docs`.