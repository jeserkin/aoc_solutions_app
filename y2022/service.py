from abc import abstractmethod
from enum import Enum
from typing import List, Union

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

    def __solve_part_one(self, problem_input: UploadedFile):
        total_score = 0
        for line in problem_input:
            opponent_move, player_move = self.__get_round_operands(line, Part.ONE)
            round_outcome = self.__get_round_outcome(opponent_move, player_move)
            total_score += self.__get_round_outcome_score(round_outcome) + self.__get_round_shape_score(player_move)
        return total_score

    def __solve_part_two(self, problem_input: UploadedFile):
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
