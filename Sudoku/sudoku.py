import operator
from functools import reduce
from typing import List
from numpy import array
import numpy as np


class Sudoku:
    def __init__(self, boards: List[array]):
        self.boards: List[array] = boards

    def __str__(self):
        res: str = '-' * 86 + "\n"
        for row in range(9):
            res += "||"
            sub_board = 3 * (row // 3)
            for column in range(9):
                cell_value: int = self.boards[sub_board][row % 3, column % 3]
                res += "  {x:^4}  |".format(x=cell_value if cell_value != 0 else " ", end=" ")
                if column % 3 == 2:
                    res += "|"
                    sub_board += 1

            res += "\n" + '-' * 86 + "\n"
            if row % 3 == 2 and row != 8:
                res += '-' * 86 + "\n"

        return res

    def __get_unique_occurrences_in_sub_board(self, sub_board_index: int) -> int:
        board_list: List = [element for row in self.boards[sub_board_index] for element in row]
        occurrences: int = reduce(operator.add, [occurrence for [value, occurrence] in
                                                 [[n, board_list.count(n)] for n in board_list if n != 0]
                                                 if occurrence == 1])
        return occurrences

    def calculate_fitness(self) -> float:
        total_rows_unique_occurrences: int = 0
        total_columns_unique_occurrences: int = 0
        total_sub_boards_unique_occurrencs: int = 0

        for index in range(9):
            row_index = index % 3
            sub_board = 3 * (index // 3)
            complete_row = []

            column_index = index % 3
            complete_column = []

            for sub_board_index in range(3):
                complete_row = np.concatenate((complete_row, self.boards[sub_board + sub_board_index][row_index]),
                                              axis=None)
                complete_column = np.concatenate((complete_column,
                                                  self.boards[3 * sub_board_index + (index // 3)][:, column_index]),
                                                 axis=None)
            column_list = list(complete_column)
            total_columns_unique_occurrences += reduce(operator.add, [occurrence for [value, occurrence] in
                                                                      [[n, column_list.count(n)] for n in column_list
                                                                       if n != 0]
                                                                      if occurrence == 1])
            row_list = list(complete_row)
            total_rows_unique_occurrences += reduce(operator.add, [occurrence for [value, occurrence] in
                                                                   [[n, row_list.count(n)] for n in row_list if n != 0]
                                                                   if occurrence == 1])

            total_sub_boards_unique_occurrencs += self.__get_unique_occurrences_in_sub_board(index)

        rows_score: float = total_rows_unique_occurrences / 9
        columns_score: float = total_columns_unique_occurrences / 9
        sub_boards_score: float = total_sub_boards_unique_occurrencs / 9

        fitness: float = (rows_score + columns_score + sub_boards_score) / 27

        return fitness


def make_mock() -> List[array]:  # funcao para gerar um sudoku mockado para testes
    sub_board1 = array([[0, 0, 0], [0, 0, 2], [0, 0, 7]])
    sub_board2 = array([[0, 0, 0], [7, 0, 9], [8, 0, 0]])
    sub_board3 = array([[0, 5, 3], [0, 4, 0], [0, 0, 0]])
    sub_board4 = array([[0, 3, 0], [0, 0, 0], [0, 8, 9]])
    sub_board5 = array([[0, 0, 0], [9, 0, 1], [0, 0, 2]])
    sub_board6 = array([[0, 0, 6], [0, 0, 0], [0, 0, 7]])
    sub_board7 = array([[4, 0, 0], [1, 0, 0], [8, 0, 0]])
    sub_board8 = array([[0, 0, 0], [0, 6, 0], [0, 4, 0]])
    sub_board9 = array([[2, 0, 0], [9, 0, 0], [0, 0, 0]])

    boards: List = [sub_board1, sub_board2, sub_board3, sub_board4, sub_board5, sub_board6,
                    sub_board7, sub_board8, sub_board9]
    return boards


def main():
    # tabuleiro mockado para testes
    mock = make_mock()

    sudoku: Sudoku = Sudoku(mock)

    print(sudoku)
    print("Fitness: ", sudoku.calculate_fitness())


if __name__ == "__main__":
    main()
