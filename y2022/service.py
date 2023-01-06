from ninja import UploadedFile

from y2022.models import Part, Solution
from typing import List


class Day1Resolver:

    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
            Solution(part=Part.TWO.value, result=self.__solve_part_two(problem_input))
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> int:
        elfs = self.__get_each_elf_calories(problem_input)
        return max(elfs)

    def __solve_part_two(self, problem_input: UploadedFile) -> int:
        elfs = self.__get_each_elf_calories(problem_input)
        elfs.sort(reverse=True)
        return sum(elfs[0:3])

    def __get_each_elf_calories(self, problem_input: UploadedFile) -> []:
        elfs = []
        current_elf_cal = 0
        for line in problem_input:
            decoded_line = line.decode()
            if decoded_line.strip() == '':
                elfs.append(current_elf_cal)
                current_elf_cal = 0
            else:
                current_elf_cal += int(decoded_line.strip())
        return elfs
