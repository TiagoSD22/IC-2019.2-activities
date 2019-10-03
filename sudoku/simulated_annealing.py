import copy
import random
from math import exp
from typing import Dict, List, Tuple
from state import State
from sudoku import Sudoku


class SimulatedAnnealingSudokuSolver:
    def __init__(self, initial_sudoku_problem: Sudoku, stale_limit: int = 500):
        self.initial_sudoku_problem = initial_sudoku_problem
        self.fixed_positions_dict = self.__find_fixed_positions()
        self.stale_limit = stale_limit

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

    @staticmethod
    def apply_heuristic(current_state: State, current_score) -> Tuple[State, float]:
        not_optimized_rows: List[int] = []
        not_optimized_columns: List[int] = []
        not_optimized_rows_group: Dict[int, List[int]] = dict()
        not_optimized_columns_group: Dict[int, List[int]] = dict()
        for row_index, row_score in current_state.sudoku_problem.rows_quality_dict.items():
            if row_score != 9:
                key = row_index // 3
                if key not in not_optimized_rows_group.keys():
                    not_optimized_rows_group[key] = [row_index]
                else:
                    group = copy.deepcopy(not_optimized_rows_group[key])
                    group.append(row_index)
                    not_optimized_rows_group[key] = group
                not_optimized_rows.append(row_index)

        for column_index, column_score in current_state.sudoku_problem.columns_quality_dict.items():
            if column_score != 9:
                key = column_index // 3
                if key not in not_optimized_columns_group.keys():
                    not_optimized_columns_group[key] = [column_index]
                else:
                    group = copy.deepcopy(not_optimized_columns_group[key])
                    group.append(column_index)
                    not_optimized_columns_group[key] = group
                not_optimized_columns.append(column_index)

        if len(not_optimized_columns) < 2:
            collection_to_optimize = not_optimized_rows
            collection_type = "row"
        elif len(not_optimized_rows) < 2:
            collection_to_optimize = not_optimized_columns
            collection_type = "column"
        else:
            collection_type, collection_to_optimize = random.choice([("column", not_optimized_columns),
                                                                     ("row", not_optimized_rows)])

        possible_rows = []
        possible_columns = []
        if collection_type == "row":
            for group, index_list in not_optimized_rows_group.items():
                if len(index_list) >= 2:
                    possible_rows.append(index_list)
            index = random.choice(possible_rows)
            position1 = index[0]
            position2 = index[1]

        else:
            for group, index_list in not_optimized_columns_group.items():
                if len(index_list) >= 2:
                    possible_columns.append(index_list)
            index = random.choice(possible_columns)
            position1 = index[0]
            position2 = index[1]

        res = current_state.perform_local_search(collection_type, (position1 % 3, position2 % 3), current_score)
        if res is not None:
            new_sudoku, new_score = res
            new_state: State = State(new_sudoku)
            return new_state, new_score
        else:
            if len(not_optimized_rows) <= 2 and len(not_optimized_columns) <= 2:
                return None
            return current_state, current_score

    def solve(self) -> Tuple[State, float]:
        current_state: State = self.__generate_first_state()
        current_score: float = current_state.get_score()
        temperature = 500000000
        stale_points = 0
        print("Estado inicial:\n{}\nPontuacao: {}".format(current_state, current_score))
        while temperature > 0 and current_score != 1:
            possible_best_state: State = State(copy.deepcopy(current_state.sudoku_problem))
            possible_best_state.disturb(self.fixed_positions_dict)
            print("\n\nEstado gerado:\n{}".format(possible_best_state))
            possible_best_score = possible_best_state.get_score()
            print("Pontuacao: ", possible_best_score)
            delta_score = possible_best_score - current_score
            accept_new_state: bool = False

            if delta_score > 0:
                accept_new_state = True
                stale_points = 0
            elif exp(delta_score/temperature) > random.random():
                accept_new_state = True
            if accept_new_state:
                print("Estado aceito")
                current_score = possible_best_score
                current_state = possible_best_state
            else:
                print("Estado NAO aceito")
                stale_points += 1

            if stale_points > self.stale_limit:
                res = self.apply_heuristic(current_state, current_score)
                if res is not None:
                    current_state, current_score = res
                else:  # recomecar
                    temperature = 500000000
                    current_state = self.__generate_first_state()
                    current_score = current_state.get_score()
                stale_points = 0

            temperature *= 0.6

        return current_state, current_score

