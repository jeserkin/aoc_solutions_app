import string
from abc import abstractmethod
from enum import Enum
from typing import List, Union, Generator

from ninja import UploadedFile

from y2022.models import Part, Solution


class Resolver:
    @abstractmethod
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        pass


class Day1Resolver(Resolver):
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


class Day2OpponentMove(Enum):
    ROCK = 'A'
    PAPER = 'B'
    SCISSORS = 'C'


class Day2PlayerMove(Enum):
    ROCK = 'X'
    PAPER = 'Y'
    SCISSORS = 'Z'


class Day2RoundOutcome(Enum):
    LOSS = 'X'
    DRAW = 'Y'
    WIN = 'Z'


class Day2Resolver(Resolver):

    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
            Solution(part=Part.TWO.value, result=self.__solve_part_two(problem_input))
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> int:
        total_score = 0
        for line in problem_input:
            opponent_move, player_move = self.__get_round_operands(line, Part.ONE)
            round_outcome = self.__get_round_outcome(opponent_move, player_move)
            total_score += self.__get_round_outcome_score(round_outcome) + self.__get_round_shape_score(player_move)
        return total_score

    def __solve_part_two(self, problem_input: UploadedFile) -> int:
        total_score = 0
        for line in problem_input:
            opponent_move, round_outcome = self.__get_round_operands(line, Part.TWO)
            shape_outcome_score = self.__get_player_shape_outcome_score(opponent_move, round_outcome)
            total_score += self.__get_round_outcome_score(round_outcome) + shape_outcome_score
        return total_score

    def __get_round_operands(self, input_line: bytes, part: Part) -> ():
        decoded_line = input_line.decode().strip()
        if part == part.ONE:
            opponent_move, _, player_move = list(decoded_line)
            return Day2OpponentMove(opponent_move), Day2PlayerMove(player_move)
        else:
            opponent_move, _, player_round_outcome = list(decoded_line)
            return Day2OpponentMove(opponent_move), Day2RoundOutcome(player_round_outcome)

    def __get_round_outcome_score(self, round_outcome: Day2RoundOutcome) -> int:
        if round_outcome == Day2RoundOutcome.DRAW:
            return 3
        elif round_outcome == Day2RoundOutcome.WIN:
            return 6
        else:
            return 0

    def __get_round_outcome(self, opponent_move: Day2OpponentMove, player_move: Day2PlayerMove) -> Day2RoundOutcome:
        if self.__is_draw(opponent_move, player_move):
            return Day2RoundOutcome.DRAW
        elif self.__is_win(opponent_move, player_move):
            return Day2RoundOutcome.WIN
        else:
            return Day2RoundOutcome.LOSS

    def __is_draw(self, opponent_move: Day2OpponentMove, player_move: Day2PlayerMove) -> bool:
        if opponent_move == Day2OpponentMove.ROCK and player_move == Day2PlayerMove.ROCK:
            return True
        elif opponent_move == Day2OpponentMove.PAPER and player_move == Day2PlayerMove.PAPER:
            return True
        elif opponent_move == Day2OpponentMove.SCISSORS and player_move == Day2PlayerMove.SCISSORS:
            return True
        return False

    def __is_win(self, opponent_move: Day2OpponentMove, player_move: Day2PlayerMove) -> bool:
        if opponent_move == Day2OpponentMove.ROCK and player_move == Day2PlayerMove.PAPER:
            return True
        elif opponent_move == Day2OpponentMove.PAPER and player_move == Day2PlayerMove.SCISSORS:
            return True
        elif opponent_move == Day2OpponentMove.SCISSORS and player_move == Day2PlayerMove.ROCK:
            return True
        return False

    def __get_round_shape_score(self, move: Union[Day2PlayerMove, Day2OpponentMove]) -> int:
        if move in [Day2PlayerMove.ROCK, Day2OpponentMove.ROCK]:
            return 1
        elif move in [Day2PlayerMove.PAPER, Day2OpponentMove.PAPER]:
            return 2
        else:
            return 3

    def __get_player_shape_outcome_score(self, opponent_move: Day2OpponentMove, round_outcome: Day2RoundOutcome) -> int:
        draw_encounters = [
            (Day2OpponentMove.ROCK, Day2PlayerMove.ROCK),
            (Day2OpponentMove.PAPER, Day2PlayerMove.PAPER),
            (Day2OpponentMove.SCISSORS, Day2PlayerMove.SCISSORS),
        ]

        if round_outcome == Day2RoundOutcome.DRAW:
            encounter = [encounter for encounter in draw_encounters if encounter[0] == opponent_move][0]
            player_move = encounter[1]
            shape_score = self.__get_round_shape_score(player_move)
        elif round_outcome == Day2RoundOutcome.WIN:
            if opponent_move == Day2OpponentMove.SCISSORS:
                shape_score = 1
            else:
                shape_score = self.__get_round_shape_score(opponent_move) + 1
        else:
            if opponent_move == Day2OpponentMove.ROCK:
                shape_score = 3
            else:
                shape_score = self.__get_round_shape_score(opponent_move) - 1

        return shape_score


class Day3Resolver(Resolver):
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
            Solution(part=Part.TWO.value, result=self.__solve_part_two(problem_input)),
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> int:
        priorities_sum = 0

        for line in problem_input:
            rucksack_compartment_items = self.__get_rucksack_compartment_items(line)
            priorities_sum += self.__get_misplaced_item_type_priority(*rucksack_compartment_items)
        return priorities_sum

    def __solve_part_two(self, problem_input: UploadedFile) -> int:
        priorities_sum = 0
        for elf_group in self.__get_elf_group(problem_input, 3):
            priorities_sum += self.__find_elf_group_badge_priority(elf_group)
        return priorities_sum

    def __get_rucksack_compartment_items(self, raw_input: bytes) -> ():
        decoded_line = raw_input.decode().strip()
        decoded_line_length = len(decoded_line)
        split = int(decoded_line_length / 2)
        return decoded_line[0:split], decoded_line[split:]

    def __get_misplaced_item_type_priority(self, compartment_one: str, compartment_two: str) -> int:
        for item in compartment_one:
            if compartment_two.count(item) > 0:
                return self.__get_item_type_priority(item)
        return 0

    def __get_elf_group(self, problem_input: UploadedFile, size: int) -> Generator:
        group = []
        for raw_input in problem_input:
            decoded_line = raw_input.decode().strip()
            group.append(decoded_line)

            if len(group) == size:
                yield tuple(group)
                group = []

    def __find_elf_group_badge_priority(self, elf_group: ()) -> int:
        elf_group_unique_items = set(''.join(elf_group))
        for item in elf_group_unique_items:
            group_check = [elf_group_items for elf_group_items in elf_group if item in elf_group_items]
            if len(group_check) == len(elf_group):
                return self.__get_item_type_priority(item)
        return 0

    def __get_item_type_priority(self, item: str) -> int:
        item_types = list(string.ascii_lowercase) + list(string.ascii_uppercase)
        return item_types.index(item) + 1


class Day4Resolver(Resolver):
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
            Solution(part=Part.TWO.value, result=self.__solve_part_two(problem_input)),
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> int:
        fully_contained_sections = 0
        for line in problem_input:
            assignment_pairs = self.__get_section_assignment_pairs(line)
            fully_contained_sections += int(self.__is_any_section_fully_contained(assignment_pairs))
        return fully_contained_sections

    def __solve_part_two(self, problem_input: UploadedFile) -> int:
        overlapping_sections = 0
        for line in problem_input:
            assignment_pairs = self.__get_section_assignment_pairs(line)
            overlapping_sections += int(self.__is_any_section_overlapping(assignment_pairs))
        return overlapping_sections

    def __get_section_assignment_pairs(self, raw_input: bytes) -> []:
        decoded_line = raw_input.decode().strip()
        pairs = decoded_line.split(',')
        sections = []
        for pair in pairs:
            sections.append(tuple(int(x) for x in pair.split('-')))
        return sections

    def __is_any_section_fully_contained(self, assignment_pairs: []) -> bool:
        pair_one, pair_two = assignment_pairs

        if pair_one[0] >= pair_two[0] and pair_one[1] <= pair_two[1]:
            return True
        elif pair_two[0] >= pair_one[0] and pair_two[1] <= pair_one[1]:
            return True

        return False

    def __is_any_section_overlapping(self, assignment_pairs: []) -> bool:
        pair_one, pair_two = assignment_pairs

        if self.__in_range(pair_two, pair_one[0]):
            return True
        elif self.__in_range(pair_two, pair_one[1]):
            return True
        elif self.__in_range(pair_one, pair_two[0]):
            return True
        elif self.__in_range(pair_one, pair_two[1]):
            return True

        return False

    def __in_range(self, limits: (), value_to_check: int) -> bool:
        a, b = limits

        if a <= value_to_check <= b:
            return True

        return False
