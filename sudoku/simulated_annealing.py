import copy
import random
from math import exp
from typing import Dict, List, Tuple

from state import State
from sudoku import Sudoku


class SimulatedAnnealingSudokuSolver:
    def __init__(self, initial_sudoku_problem: Sudoku):
        self.initial_sudoku_problem = initial_sudoku_problem
        self.fixed_positions_dict = self.__find_fixed_positions()

    def __find_fixed_positions(self) -> Dict[int, List[int]]:
        fixed_positions_dict: Dict[int, List[int]] = dict()
        for board_index in range(9):
            board_fixed_positions: List[int] = []
            for row in range(3):
                for column in range(3):
                    board = self.initial_sudoku_problem.boards[board_index]
                    if board[row, column] != 0:
                        board_fixed_positions.append(3*row + column)
            fixed_positions_dict[board_index] = board_fixed_positions
        return fixed_positions_dict

    def __generate_first_state(self) -> State:
        values: List[int] = [v for v in range(1, 10)]
        filling_sudoku: Sudoku = copy.deepcopy(self.initial_sudoku_problem)
        for row in range(9):
            for column in range(9):
                sub_board: int = 3 * (row // 3) + (column // 3)
                cell_value: int = self.initial_sudoku_problem.boards[sub_board][
                    row % 3, column % 3
                ]
                if cell_value == 0:  # celula vazia
                    # preenchendo a celula vazia com um valor ainda nao usado na sua submatriz para respeitar a regra
                    # de valores unicos em cada submatriz
                    new_value: int = random.choice(
                        [
                            x
                            for x in values
                            if x
                               not in [
                                   value
                                   for row in filling_sudoku.boards[sub_board]
                                   for value in row
                               ]
                        ]
                    )
                    filling_sudoku.boards[sub_board][row % 3, column % 3] = new_value

        first_state: State = State(filling_sudoku)
        return first_state

    def solve(self) -> Tuple[State, float]:
        current_state: State = self.__generate_first_state()
        current_score: float = current_state.get_score()
        temperature = 500000000
        while temperature > 0 and current_score != 1:
            possible_best_state: State = State(copy.deepcopy(current_state.sudoku_problem))
            possible_best_state.disturb(self.fixed_positions_dict)
            possible_best_score = possible_best_state.get_score()
            delta_score = possible_best_score - current_score
            accept_new_state: bool = False
            if delta_score > 0:
                accept_new_state = True
            elif exp(delta_score/temperature) > random.random():
                accept_new_state = True
            if accept_new_state:
                current_score = possible_best_score
                current_state = possible_best_state

            #print("Melhor score: ", current_score)

            temperature *= 0.6

        return current_state, current_score

