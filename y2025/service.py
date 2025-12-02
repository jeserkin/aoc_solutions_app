from typing import List

from ninja import UploadedFile

from common.models import Part, Solution, Resolver


class Day1Resolver(Resolver):
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> int:
        print(problem_input)
        return 0