import operator
from functools import reduce
from typing import List
from numpy import array
import numpy as np


class Sudoku:
    def __init__(self, boards: List[array]):
        self.boards: List[array] = boards

    def __str__(self):
        res: str = "-" * 86 + "\n"
        for row in range(9):
            res += "||"
            sub_board = 3 * (row // 3)
            for column in range(9):
                cell_value: int = self.boards[sub_board][row % 3, column % 3]
                res += "  {x:^4}  |".format(
                    x=cell_value if cell_value != 0 else " ", end=" "
                )
                if column % 3 == 2:
                    res += "|"
                    sub_board += 1

            res += "\n" + "-" * 86 + "\n"
            if row % 3 == 2 and row != 8:
                res += "-" * 86 + "\n"

        return res

    def get_sub_board_score(self, sub_board_index: int) -> int:
        board_list: List = [
            element for row in self.boards[sub_board_index] for element in row
        ]
        occurrences: int = reduce(
            operator.add,
            [
                occurrence
                for [value, occurrence] in [
                    [n, board_list.count(n)] for n in board_list if n != 0
                ]
                if occurrence == 1
            ],
            0,
        )
        return occurrences

    def get_row(self, row_index):
        sub_board = 3 * (row_index // 3)
        complete_row = []

        for sub_board_index in range(3):
            complete_row = np.concatenate(
                (complete_row, self.boards[sub_board + sub_board_index][row_index % 3]),
                axis=None,
            )
        return complete_row

    def get_column(self, column_index):
        sub_board = column_index // 3
        complete_column = []

        for sub_board_index in range(3):
            complete_column = np.concatenate(
                (
                    complete_column,
                    self.boards[3 * sub_board_index + sub_board][:, column_index % 3],
                ),
                axis=None,
            )
        return complete_column

    def get_row_score(self, row_index: int) -> int:
        complete_row = self.get_row(row_index)
        row_list = list(complete_row)
        row_score = reduce(
            operator.add,
            [
                occurrence
                for [value, occurrence] in [
                    [n, row_list.count(n)] for n in row_list if n != 0
                ]
                if occurrence == 1
            ],
            0,
        )
        return row_score

    def get_column_score(self, column_index: int) -> int:
        complete_column = self.get_column(column_index)
        column_list = list(complete_column)
        column_score = reduce(
            operator.add,
            [
                occurrence
                for [value, occurrence] in [
                    [n, column_list.count(n)] for n in column_list if n != 0
                ]
                if occurrence == 1
            ],
            0,
        )
        return column_score

    def calculate_fitness(self) -> float:
        total_rows_unique_occurrences: int = 0
        total_columns_unique_occurrences: int = 0
        total_sub_boards_unique_occurrences: int = 0

        for index in range(9):
            total_columns_unique_occurrences += self.get_column_score(index)
            total_rows_unique_occurrences += self.get_row_score(index)
            total_sub_boards_unique_occurrences += self.get_sub_board_score(index)

        rows_score: float = total_rows_unique_occurrences / 9
        columns_score: float = total_columns_unique_occurrences / 9
        sub_boards_score: float = total_sub_boards_unique_occurrences / 9

        fitness: float = (rows_score + columns_score + sub_boards_score) / 27

        return fitness
