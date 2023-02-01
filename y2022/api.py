from enum import Enum
from typing import List

from ninja import Router, File
from ninja.files import UploadedFile

from y2022.models import Solution
from y2022.service import Day1Resolver, Day2Resolver, Day3Resolver, Day4Resolver, Day5Resolver, Day6Resolver, \
    Day7Resolver, Day8Resolver, Day9Resolver, Day10Resolver

router = Router(tags=["2022"])


class DaySelection(str, Enum):
    DAY_1 = '1',
    DAY_2 = '2',
    DAY_3 = '3',
    DAY_4 = '4',
    DAY_5 = '5',
    DAY_6 = '6',
    DAY_7 = '7',
    DAY_8 = '8',
    DAY_9 = '9',
    DAY_10 = '10',
    DAY_11 = '11',
    DAY_12 = '12',
    DAY_13 = '13',
    DAY_14 = '14',
    DAY_15 = '15',
    DAY_16 = '16',
    DAY_17 = '17',
    DAY_18 = '18',
    DAY_19 = '19',
    DAY_20 = '20',
    DAY_21 = '21',
    DAY_22 = '22',
    DAY_23 = '23',
    DAY_24 = '24',
    DAY_25 = '25',


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


@router.post('/day/6', response=List[Solution], summary='Day 6 solutions')
def day6_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 6 problem and provides solution for both parts
    """
    resolver = Day6Resolver()
    return list(resolver.resolve(problem_input))


@router.post('/day/7', response=List[Solution], summary='Day 7 solutions')
def day7_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 7 problem and provides solution for both parts
    """
    resolver = Day7Resolver()
    return list(resolver.resolve(problem_input))


@router.post('/day/8', response=List[Solution], summary='Day 8 solutions')
def day8_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 8 problem and provides solution for both parts
    """
    resolver = Day8Resolver()
    return list(resolver.resolve(problem_input))


@router.post('/day/9', response=List[Solution], summary='Day 9 solutions')
def day9_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 9 problem and provides solution for both parts
    """
    resolver = Day9Resolver()
    return list(resolver.resolve(problem_input))


@router.post('/day/10', response=List[Solution], summary='Day 10 solutions')
def day10_solution(request, problem_input: UploadedFile = File(...)):
    """
    Solves Day 10 problem and provides solution for both parts
    """
    resolver = Day10Resolver()
    return list(resolver.resolve(problem_input))
