from abc import abstractmethod
from enum import Enum
from typing import List

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
            opponent_move, player_move = self.__get_round_moves(line, Part.ONE)
            total_score += self.__get_round_score(opponent_move, player_move)
        return total_score

    def __solve_part_two(self, problem_input: UploadedFile):
        total_score = 0
        for line in problem_input:
            opponent_move, player_move = self.__get_round_moves(line, Part.TWO)
            total_score += self.__get_round_score(opponent_move, player_move)
        return total_score

    def __get_round_moves(self, input_line: bytes, part: Part) -> ():
        decoded_line = input_line.decode().strip()
        if part == part.ONE:
            opponent_move, _, player_move = list(decoded_line)
            return Day2OpponentMove(opponent_move), Day2PlayerMove(player_move)
        else:
            """
            This probably can be solved more easily since you already have data to calculate round score.
            Outcome tells the weight for round outcome -> __get_round_outcome_score.
            Opponent move in case of draw, tells the weight of your shape -> ROCK == ROCK -> 1.
            So basically if we assume:
              ROCK = 1
              PAPER = 2
              SCISSORS = 3
            Then win for us will be opponent_move == SCISSORS ? 1 : opponent_move.weight + 1
            And loss would be opponent_move == ROCK ? 3 : opponent_move.weight - 1
            """
            opponent_move, _, player_round_outcome = list(decoded_line)
            opponent_move = Day2OpponentMove(opponent_move)
            player_move = self.__get_player_move(opponent_move, Day2RoundOutcome(player_round_outcome))
            return opponent_move, player_move

    def __get_player_move(self, opponent_move: Day2OpponentMove, round_outcome: Day2RoundOutcome) -> Day2PlayerMove:
        if round_outcome == Day2RoundOutcome.WIN:
            if self.__is_win(opponent_move, Day2PlayerMove.ROCK):
                return Day2PlayerMove.ROCK
            elif self.__is_win(opponent_move, Day2PlayerMove.PAPER):
                return Day2PlayerMove.PAPER
            else:
                return Day2PlayerMove.SCISSORS
        elif round_outcome == Day2RoundOutcome.DRAW:
            if self.__is_draw(opponent_move, Day2PlayerMove.ROCK):
                return Day2PlayerMove.ROCK
            elif self.__is_draw(opponent_move, Day2PlayerMove.PAPER):
                return Day2PlayerMove.PAPER
            else:
                return Day2PlayerMove.SCISSORS
        else:
            if self.__is_loss(opponent_move, Day2PlayerMove.ROCK):
                return Day2PlayerMove.ROCK
            elif self.__is_loss(opponent_move, Day2PlayerMove.PAPER):
                return Day2PlayerMove.PAPER
            else:
                return Day2PlayerMove.SCISSORS

    def __get_round_score(self, opponent_move: Day2OpponentMove, player_move: Day2PlayerMove) -> int:
        return self.__get_round_outcome_score(opponent_move, player_move) + self.__get_round_shape_score(player_move)

    def __get_round_outcome_score(self, opponent_move: Day2OpponentMove, player_move: Day2PlayerMove) -> int:
        if self.__is_draw(opponent_move, player_move):
            return 3
        elif self.__is_win(opponent_move, player_move):
            return 6
        else:
            return 0

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

    def __is_loss(self, opponent_move: Day2OpponentMove, player_move: Day2PlayerMove) -> bool:
        if opponent_move == Day2OpponentMove.ROCK and player_move == Day2PlayerMove.SCISSORS:
            return True
        elif opponent_move == Day2OpponentMove.PAPER and player_move == Day2PlayerMove.ROCK:
            return True
        elif opponent_move == Day2OpponentMove.SCISSORS and player_move == Day2PlayerMove.PAPER:
            return True
        return False

    def __get_round_shape_score(self, player_move: Day2PlayerMove) -> int:
        if player_move == Day2PlayerMove.ROCK:
            return 1
        elif player_move == Day2PlayerMove.PAPER:
            return 2
        else:
            return 3
