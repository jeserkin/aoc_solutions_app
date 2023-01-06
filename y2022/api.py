from typing import List

from ninja import Router, File
from ninja.files import UploadedFile

from y2022.models import Solution
from y2022.service import Day1Resolver

router = Router(tags=["2022"])


@router.post('/day/1', response=List[Solution], summary='Day 1 solutions')
def day1_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 1 problem and provides solution for both parts
    """
    resolver = Day1Resolver()
    return list(resolver.resolve(problem_input))
