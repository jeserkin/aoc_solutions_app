# Advent of Code 2022, 2025 solutions

## Requirements
* Python 3.14.0
* Poetry 2.2.1
* Django 5.2.9
* Django-ninja 1.5.0

## Installing Python
https://www.python.org/downloads/release/python-3111/

## Installing Poetry
https://python-poetry.org/docs/#installation  
`python pipx.pyz install poetry`
### Before running install dependencies
`poetry install`


## Running project with Poetry
To start the application `poetry run python manage.py runserver`.

Once application is running, you can access API at `http://localhost:8000/api/docs`.

## How to extend
### For an additional year
1. Create new folder with year number, e.g. `y2026`
2. Copy files from the previous year directory
3. Make necessary changes so that 2025 is replaced with 2026
4. In `app/api.py` add new routing and new router

### For a daily solution
1. Add new endpoint in `api.py`
2. Can be copied from the previous year. Make sure that the correct router is referenced.
3. Add a new class in `service.py` for a specific day, e.g. `Day1Resolver`
   * It extends abstract `Resolver`  class and implements `resolve` method.
   * It should return a list of Solution objects
4. Then solve the problem and set results in the Solution objects.