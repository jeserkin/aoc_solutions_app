from typing import List

from ninja import Router, File
from ninja.files import UploadedFile

from y2022.models import Solution
from y2022.service import Day1Resolver, Day2Resolver, Day3Resolver, Day4Resolver, Day5Resolver

router = Router(tags=["2022"])


@router.post('/day/1', response=List[Solution], summary='Day 1 solutions')
def day1_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 1 problem and provides solution for both parts
    """
    resolver = Day1Resolver()
    return list(resolver.resolve(problem_input))


@router.post('/day/2', response=List[Solution], summary='Day 2 solutions')
def day2_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 2 problem and provides solution for both parts
    """
    resolver = Day2Resolver()
    return list(resolver.resolve(problem_input))


@router.post('/day/3', response=List[Solution], summary='Day 3 solutions')
def day3_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 3 problem and provides solution for both parts
    """
    resolver = Day3Resolver()
    return list(resolver.resolve(problem_input))


@router.post('/day/4', response=List[Solution], summary='Day 4 solutions')
def day4_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 4 problem and provides solution for both parts
    """
    resolver = Day4Resolver()
    return list(resolver.resolve(problem_input))


@router.post('/day/5', response=List[Solution], summary='Day 5 solutions')
def day5_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 5 problem and provides solution for both parts
    """
    resolver = Day5Resolver()
    return list(resolver.resolve(problem_input))
