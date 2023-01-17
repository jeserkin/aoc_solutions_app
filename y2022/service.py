import re
import string
from abc import abstractmethod
from enum import Enum
from functools import reduce
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


class Day5Resolver(Resolver):
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
            Solution(part=Part.TWO.value, result=self.__solve_part_two(problem_input)),
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> str:
        input_as_list = self.__convert_to_list(problem_input)
        stacks_of_crates, procedure = self.__get_main_peaces(input_as_list)
        crates_map = self.__create_crates_map(stacks_of_crates)
        self.__operate_crane(crates_map, procedure, Part.ONE)
        return self.__find_top_crates(crates_map)

    def __solve_part_two(self, problem_input: UploadedFile) -> str:
        input_as_list = self.__convert_to_list(problem_input)
        stacks_of_crates, procedure = self.__get_main_peaces(input_as_list)
        crates_map = self.__create_crates_map(stacks_of_crates)
        self.__operate_crane(crates_map, procedure, Part.TWO)
        return self.__find_top_crates(crates_map)

    def __convert_to_list(self, problem_input: UploadedFile) -> []:
        result = []
        for line in problem_input:
            result.append(line.decode().rstrip())
        return result

    def __get_main_peaces(self, input_as_list: []) -> ():
        split = input_as_list.index('')
        return input_as_list[0:split], input_as_list[split + 1:]

    def __create_crates_map(self, stacks_of_crates: []) -> []:
        map_size = stacks_of_crates.pop().strip()
        map_size = int(map_size[len(map_size) - 1])
        crates_map = [[] for _ in range(map_size)]
        for stack_row in stacks_of_crates:
            for idx, crate in enumerate(self.__read_map_row(stack_row)):
                if crate.strip() != '':
                    crates_map[idx].append(crate)
        return crates_map

    def __read_map_row(self, stacks_row: str) -> Generator:
        chunk_size = 3
        for i in range(0, len(stacks_row), chunk_size + 1):
            chunk = stacks_row[i:i + chunk_size]
            yield chunk

    def __operate_crane(self, crates_map: [], procedure: [], part: Part) -> None:
        for operation in procedure:
            crates_to_move, from_stack, to_stack = self.__parse_operation(operation)
            if part == Part.ONE:
                self.__execute_crate_mover_9000_operation(crates_map, crates_to_move, from_stack, to_stack)
            else:
                self.__execute_crate_mover_9001_operation(crates_map, crates_to_move, from_stack, to_stack)

    def __parse_operation(self, operation: str) -> ():
        result = re.match(r'move (\d+) from (\d+) to (\d+)', operation)
        return tuple([int(group) for group in list(result.groups())])

    def __execute_crate_mover_9000_operation(self, crates_map: [], crates_to_move: int, from_stack: int,
                                             to_stack: int) -> None:
        for _ in range(crates_to_move):
            source_stack = crates_map[from_stack - 1]
            destination_stack = crates_map[to_stack - 1]
            crate_to_move = source_stack.pop(0)
            destination_stack.insert(0, crate_to_move)

    def __execute_crate_mover_9001_operation(self, crates_map: [], crates_to_move: int, from_stack: int,
                                             to_stack: int) -> None:
        source_stack = crates_map[from_stack - 1]
        destination_stack = crates_map[to_stack - 1]
        transferable_crates = source_stack[0:crates_to_move]
        crates_map[to_stack - 1] = transferable_crates + destination_stack
        crates_map[from_stack - 1] = source_stack[crates_to_move:]

    def __find_top_crates(self, crates_map: []) -> str:
        top_crates = ''
        for crate_stack in crates_map:
            top_crates += re.match(r'\[(\w+)', crate_stack[0]).group(1)
        return top_crates


class Day6Resolver(Resolver):
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
            Solution(part=Part.TWO.value, result=self.__solve_part_two(problem_input)),
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> int:
        return self.__find_marker(problem_input, 4)

    def __solve_part_two(self, problem_input: UploadedFile) -> int:
        return self.__find_marker(problem_input, 14)

    def __find_marker(self, problem_input: UploadedFile, marker_chunk_size: int) -> int:
        for line in problem_input:
            decoded_line = line.decode().strip()
            for i in range(0, len(decoded_line)):
                chunk = decoded_line[i: i + marker_chunk_size]
                if len(chunk) == len(set(chunk)):
                    return i + marker_chunk_size
        return 0


class Day7FileType(Enum):
    DIR = 1,
    FILE = 2


class Day7File:

    def __init__(self) -> None:
        self.__type = Day7FileType.DIR
        self.__size = 0
        self.__name = '/'
        self.__parent = None
        self.__children = []

    def set_type(self, file_type: Day7FileType) -> None:
        self.__type = file_type

    def is_dir(self) -> bool:
        return self.__type == Day7FileType.DIR

    def is_file(self) -> bool:
        return self.__type == Day7FileType.FILE

    def set_size(self, size: int) -> None:
        self.__size = size

    def get_size(self) -> int:
        if self.__type == Day7FileType.DIR:
            total = 0
            for child in self.__children:
                total += child.get_size()
            return total
        else:
            return self.__size

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_parent(self, parent: 'Day7File') -> None:
        self.__parent = parent

    def get_parent(self) -> 'Day7File':
        return self.__parent

    def add_child(self, child: 'Day7File') -> None:
        if not any(child_item.get_name() == child.get_name() for child_item in self.__children):
            self.__children.append(child)

    def get_children(self) -> []:
        return self.__children


class Day7Resolver(Resolver):
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
            Solution(part=Part.TWO.value, result=self.__solve_part_two(problem_input)),
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> int:
        file_tree = self.__create_file_tree(problem_input)
        file_tree = self.__change_directory('/', file_tree)
        total = 0
        for directory in self.__find_directories(file_tree, 100000):
            total += directory.get_size()
        return total

    def __solve_part_two(self, problem_input: UploadedFile) -> int:
        file_tree = self.__create_file_tree(problem_input)
        file_tree = self.__change_directory('/', file_tree)
        filesystem_space = 70000000
        update_required_space = 30000000
        used_space = file_tree.get_size()
        free_space = filesystem_space - used_space

        best_deletion_candidate = None
        found_directories = self.__find_directories(file_tree, update_required_space)
        found_directories.sort(key=lambda x: x.get_size(), reverse=True)

        for directory in found_directories:
            if update_required_space <= (directory.get_size() + free_space):
                best_deletion_candidate = directory

        return best_deletion_candidate.get_size()

    def __create_file_tree(self, problem_input: UploadedFile) -> Day7File:
        current_directory = Day7File()

        for raw_input in problem_input:
            decoded_line = raw_input.decode().strip()
            if decoded_line[0] == '$':
                current_directory = self.__perform_command(decoded_line, current_directory)
            else:
                self.__read_file_listing(decoded_line, current_directory)

        return current_directory

    def __perform_command(self, decoded_line: str, current_directory: Day7File) -> Day7File:
        matcher = re.match(r'\$ cd (\w+|/|\.{2})', decoded_line)
        if matcher:
            return self.__change_directory(matcher.group(1), current_directory)
        else:
            return current_directory

    def __read_file_listing(self, decoded_line: str, current_directory: Day7File) -> None:
        matcher = re.match(r'(\d+)\s+([\w.]+)', decoded_line)
        if matcher:
            directory_file = self.__create_directory_file(name=matcher.group(2), size=int(matcher.group(1)))
            current_directory.add_child(directory_file)
            directory_file.set_parent(current_directory)

    def __create_directory(self, name: str) -> Day7File:
        directory = Day7File()
        directory.set_name(name)
        return directory

    def __change_directory(self, directory_name: str, current_directory: Day7File) -> Day7File:
        if directory_name == '/':
            return self.__navigate_to_root(current_directory)
        elif directory_name == '..':
            return self.__navigate_to_parent(current_directory)
        else:
            directory = self.__create_directory(directory_name)

            if isinstance(current_directory, Day7File):
                current_directory.add_child(directory)
                directory.set_parent(current_directory)

            return directory

    def __navigate_to_root(self, current_directory: Day7File) -> Day7File:
        if current_directory.get_parent() is not None:
            return self.__navigate_to_root(current_directory.get_parent())
        else:
            return current_directory

    def __navigate_to_parent(self, current_directory: Day7File) -> Day7File:
        if current_directory.get_parent() is not None:
            return current_directory.get_parent()
        else:
            return current_directory

    def __create_directory_file(self, name: str, size: int) -> Day7File:
        directory_file = Day7File()
        directory_file.set_name(name)
        directory_file.set_size(size)
        directory_file.set_type(Day7FileType.FILE)
        return directory_file

    def __find_directories(self, file_tree: Day7File, smaller_than_or_equal: int) -> []:
        found_directories = []
        for child in file_tree.get_children():
            if child.is_dir():
                found_directories += self.__find_directories(child, smaller_than_or_equal)
                if child.get_size() <= smaller_than_or_equal:
                    found_directories.append(child)
        return found_directories


class Day8Resolver(Resolver):
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        return [
            Solution(part=Part.ONE.value, result=self.__solve_part_one(problem_input)),
            Solution(part=Part.TWO.value, result=self.__solve_part_two(problem_input)),
        ]

    def __solve_part_one(self, problem_input: UploadedFile) -> int:
        grid = {}
        for row_idx, raw_input in enumerate(problem_input):
            decoded_line = raw_input.decode().strip()
            self.__read_grid(grid, decoded_line, row_idx)

        return self.__find_visible_trees(grid)

    def __solve_part_two(self, problem_input: UploadedFile) -> int:
        grid = {}
        for row_idx, raw_input in enumerate(problem_input):
            decoded_line = raw_input.decode().strip()
            self.__read_grid(grid, decoded_line, row_idx)

        return self.__calculate_trees_scenic_score(grid)

    def __read_grid(self, grid: {}, decoded_line: str, row_idx: int) -> None:
        for col_idx, tree_height in enumerate(decoded_line):
            grid[(col_idx, row_idx)] = int(tree_height)

    def __get_grid_size(self, grid: {}) -> ():
        width = max(grid.keys(), key=lambda x: x[0])[0]
        height = max(grid.keys(), key=lambda y: y[1])[1]
        # because 0 based
        return width + 1, height + 1

    def __find_visible_trees(self, grid: {}) -> int:
        grid_width, grid_height = self.__get_grid_size(grid)
        visible_trees = 0

        for position, tree_height in grid.items():
            position_x, position_y = position
            if position_x == 0 or position_x == (grid_width - 1):
                visible_trees += 1
            elif position_y == 0 or position_y == (grid_height - 1):
                visible_trees += 1
            else:
                visible_trees += self.__is_interior_tree_visible(position, tree_height, grid) is True

        return visible_trees

    def __is_interior_tree_visible(self, position: (), tree_height: int, grid: {}) -> bool:
        tree_x, tree_y = position
        hidden = {
            'N': False,
            'E': False,
            'S': False,
            'W': False
        }

        # movement from point
        step = 1
        while True:

            # not visible from top?
            if (tree_x, tree_y - step) in grid and hidden['N'] is False and \
                    grid[(tree_x, tree_y - step)] >= tree_height:
                hidden['N'] = True

            # not visible from right?
            if (tree_x + step, tree_y) in grid and hidden['E'] is False and \
                    grid[(tree_x + step, tree_y)] >= tree_height:
                hidden['E'] = True

            # not visible from bottom?
            if (tree_x, tree_y + step) in grid and hidden['S'] is False and \
                    grid[(tree_x, tree_y + step)] >= tree_height:
                hidden['S'] = True

            # not visible from left?
            if (tree_x - step, tree_y) in grid and hidden['W'] is False and \
                    grid[(tree_x - step, tree_y)] >= tree_height:
                hidden['W'] = True

            if all(hidden.values()):
                return False

            # outside grid?
            if (tree_x, tree_y - step) not in grid and \
                    (tree_x + step, tree_y) not in grid and \
                    (tree_x, tree_y + step) not in grid and \
                    (tree_x - step, tree_y) not in grid:
                return True

            step += 1

    def __calculate_trees_scenic_score(self, grid: {}) -> int:
        grid_width, grid_height = self.__get_grid_size(grid)
        scenic_score = []

        for position, tree_height in grid.items():
            position_x, position_y = position
            if position_x == 0 or position_x == (grid_width - 1):
                continue
            elif position_y == 0 or position_y == (grid_height - 1):
                continue
            else:
                scenic_score.append(self.__calculate_tree_scenic_score(position, tree_height, grid))

        return max(scenic_score)

    def __calculate_tree_scenic_score(self, position, tree_height, grid) -> int:
        tree_x, tree_y = position
        block_reached = {
            'N': False,
            'E': False,
            'S': False,
            'W': False
        }
        tree_scenic_score = {
            'N': 0,
            'E': 0,
            'S': 0,
            'W': 0
        }

        # movement from point
        step = 1
        while True:

            # not visible from top?
            if (tree_x, tree_y - step) in grid and block_reached['N'] is False:
                block_reached['N'] = grid[(tree_x, tree_y - step)] >= tree_height
                tree_scenic_score['N'] = step

            # not visible from right?
            if (tree_x + step, tree_y) in grid and block_reached['E'] is False:
                block_reached['E'] = grid[(tree_x + step, tree_y)] >= tree_height
                tree_scenic_score['E'] = step

            # not visible from bottom?
            if (tree_x, tree_y + step) in grid and block_reached['S'] is False:
                block_reached['S'] = grid[(tree_x, tree_y + step)] >= tree_height
                tree_scenic_score['S'] = step

            # not visible from left?
            if (tree_x - step, tree_y) in grid and block_reached['W'] is False:
                block_reached['W'] = grid[(tree_x - step, tree_y)] >= tree_height
                tree_scenic_score['W'] = step

            if all(block_reached.values()):
                return reduce((lambda x, y: x * y), tree_scenic_score.values())

            # outside grid?
            if (tree_x, tree_y - step) not in grid and \
                    (tree_x + step, tree_y) not in grid and \
                    (tree_x, tree_y + step) not in grid and \
                    (tree_x - step, tree_y) not in grid:
                return reduce((lambda x, y: x * y), tree_scenic_score.values())

            step += 1
