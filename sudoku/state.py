"""Classe que modela um estado, entidade utilizada durante as iteracoes do algoritmo Tempera Simulada
"""


import random
from typing import List, Dict
from sudoku import Sudoku
import logging


class State:
    def __init__(self, sudoku_problem: Sudoku, logger: logging):
        self.sudoku_problem = sudoku_problem
        self.logger = logger

    def disturb(self, fixed_positions_dict: Dict[int, List[int]]):
        """ Causa uma modficacao no estado atual trocando, aleatoriamente, duas celulas de lugar
        :param fixed_positions_dict: dicionario indicando quais as celulas sao fixas em cada submatriz
        :return None, o atributo sudoku_problem do objeto e alterado diretamente dentro do metodo
        """

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
        self.logger.debug(
            f"Submatriz escolihda: {sub_board_index}\nCelulas escolhidas: {block1_position}, {block2_position}"
        )

    def get_score(self) -> float:
        """ Retorna a quantidade de elemento unicos em uma linha
        :param None
        :return state_score: qualidade do Sudoku deste objeto baseado na heuristica de quantidade de valores unicos
        em cada linha e coluna
        """
        state_score: float = self.sudoku_problem.calculate_fitness()
        return state_score

    def __str__(self):
        return str(self.sudoku_problem)
