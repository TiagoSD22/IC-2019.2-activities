"""Classe que modela uma instancia do Sudoku e metodos auxiliares
"""

import operator
from functools import reduce
from typing import List, Dict
from numpy import array
import numpy as np
import logging


class Sudoku:
    def __init__(self, boards: List[array], logger: logging):
        self.boards: List[array] = boards
        # o dicionario auxilia a recuperar em tempo linear a qualidade de cada linha do Sudoku
        self.rows_quality_dict: Dict[int, int] = dict()
        # o dicionario auxilia a recuperar em tempo linear a qualidade de cada coluna do Sudoku
        self.columns_quality_dict: Dict[int, int] = dict()
        self.logger: logging = logger

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

    def get_row(self, row_index) -> array:
        """ Retorna uma linha do Sudoku
        :param row_index: indice da linha buscada
        :return complete_row: um objeto do tipo array contendo os 9 elementos da linha buscada
        """

        sub_board = 3 * (row_index // 3)
        complete_row: array = []

        for sub_board_index in range(3):
            complete_row = np.concatenate(
                (complete_row, self.boards[sub_board + sub_board_index][row_index % 3]),
                axis=None,
            )
        return complete_row

    def get_column(self, column_index) -> array:
        """ Retorna uma coluna do Sudoku
        :param column_index: indice da coluna buscada
        :return complete_column: um objeto do tipo array contendo os 9 elementos da coluna buscada
        """

        sub_board = column_index // 3
        complete_column: array = []

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
        """ Retorna a quantidade de elemento unicos em uma linha
        :param row_index: indice da linha buscada
        :return row_score: um inteiro representando a quantidade elementos nao repetidos na linha
        """

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
        self.rows_quality_dict[row_index] = row_score
        self.logger.debug(f"Pontuacao da linha {row_index}: {row_score}")
        return row_score

    def get_column_score(self, column_index: int) -> int:
        """ Retorna a quantidade de elemento unicos em uma coluna
        :param column_index: indice da coluna buscada
        :return column_score: um inteiro representando a quantidade elementos nao repetidos na coluna
        """

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
        self.columns_quality_dict[column_index] = column_score
        self.logger.debug(f"Pontuacao da coluna {column_index}: {column_score}")
        return column_score

    def calculate_fitness(self) -> float:
        """ Retorna a qualidade de um Sudoku, dada pela quantidade total de elementos unicos em cada linha e coluna
        dividiso por 18, sendo um valor de ponto flutuante entre 0(pior caso) e 1(Sudoku resolvido)
        :param None
        :return fitness: um valor float representando o quao perto o Sudoku esta de ser resolvido, utilizando a
        heuristica de repeticoes em cada linha e coluna
        """

        total_rows_unique_occurrences: int = 0
        total_columns_unique_occurrences: int = 0

        for index in range(9):
            total_columns_unique_occurrences += self.get_column_score(index)
            total_rows_unique_occurrences += self.get_row_score(index)

        rows_score: float = total_rows_unique_occurrences / 9
        columns_score: float = total_columns_unique_occurrences / 9

        fitness: float = (rows_score + columns_score) / 18

        return fitness
