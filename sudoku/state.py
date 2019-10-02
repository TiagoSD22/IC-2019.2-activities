import random
from typing import List, Dict

from sudoku import Sudoku


class State:
    def __init__(self, sudoku_problem: Sudoku):
        self.sudoku_problem = sudoku_problem

    def disturb(self, fixed_positions_dict: Dict[int, List[int]]):
        sub_board_index: int = random.choice([index for index in range(9)])
        sub_board_fixed_positions: List[int] = fixed_positions_dict[sub_board_index]
        swappable_cells = [x for x in range(9) if x not in sub_board_fixed_positions]

        block1_position = random.choice(swappable_cells)
        swappable_cells.remove(block1_position)
        block2_position = random.choice(swappable_cells)

        chosen_board = self.sudoku_problem.boards[sub_board_index]
        chosen_board[block1_position // 3, block1_position % 3], chosen_board[
            block2_position // 3, block2_position % 3
        ] = (
            chosen_board[block2_position // 3, block2_position % 3],
            chosen_board[block1_position // 3, block1_position % 3],
        )

    def get_score(self):
        return self.sudoku_problem.calculate_fitness()

    def __str__(self):
        return str(self.sudoku_problem)
