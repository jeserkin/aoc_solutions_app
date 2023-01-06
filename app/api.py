from ninja import NinjaAPI

from y2022.api import router as y2022_router

api = NinjaAPI(
    title='Advent of Code 2022- solutions',
    description='Solutions for 2022- problems implemented in `Python`',
    version='1.0.0'
)

api.add_router('year/2022', y2022_router)
