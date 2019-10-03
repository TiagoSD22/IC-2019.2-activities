import copy
import random
from typing import List, Dict, Tuple
from sudoku import Sudoku


class State:
    def __init__(self, sudoku_problem: Sudoku):
        self.sudoku_problem = sudoku_problem

    def disturb(self, fixed_positions_dict: Dict[int, List[int]]):
        sub_board_index: int = random.choice([index for index in range(9)])
        sub_board_fixed_positions: List[int] = fixed_positions_dict[sub_board_index]
        swappable_cells = [x for x in range(9) if x not in sub_board_fixed_positions]

        block1_position, block2_position = random.sample(swappable_cells, 2)

        chosen_board = self.sudoku_problem.boards[sub_board_index]
        chosen_board[block1_position // 3, block1_position % 3], chosen_board[
            block2_position // 3, block2_position % 3
        ] = (
            chosen_board[block2_position // 3, block2_position % 3],
            chosen_board[block1_position // 3, block1_position % 3],
        )
        print(
            "Submatriz escolihda: {}\nCelulas escolhidas: {}, {}".format(
                sub_board_index, block1_position, block2_position
            )
        )

    def perform_local_search(
        self,
        collection_searching: str,
        search_index: Tuple[int, int],
        best_score: float,
    ) -> Tuple[Sudoku, float]:
        if collection_searching == "row":
            row1_index, row2_index = search_index
            for column_index in range(9):
                copy_sudoku: Sudoku = copy.deepcopy(self.sudoku_problem)
                sub_board_index: int = 3 * (row1_index // 3) + column_index // 3
                board = copy_sudoku.boards[sub_board_index]
                col = column_index % 3
                board[row1_index, col], board[row2_index, col] = board[row2_index, col], board[row1_index, col]
                new_score: float = copy_sudoku.calculate_fitness()
                if new_score > best_score:
                    return copy_sudoku, new_score

        elif collection_searching == "column":
            column1_index, column2_index = search_index
            for row_index in range(9):
                copy_sudoku: Sudoku = copy.deepcopy(self.sudoku_problem)
                sub_board_index: int = 3 * (column1_index // 3) + row_index // 3
                board = copy_sudoku.boards[sub_board_index]
                row = row_index % 3
                board[row, column1_index], board[row, column2_index] = board[row, column2_index], board[row, column1_index]
                new_score: float = copy_sudoku.calculate_fitness()
                if new_score > best_score:
                    return copy_sudoku, new_score

        return None

    def get_score(self):
        return self.sudoku_problem.calculate_fitness()

    def __str__(self):
        return str(self.sudoku_problem)
