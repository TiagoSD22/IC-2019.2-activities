#!/usr/bin/env python
"""Implementa um solucionador para um Sudoku tradicional

Este código implementa classes e modelos para solucionar instâncias de um problema Sudoku tradicional com 9 linhas
e 9 coulnas. A estrategia utilizada para resolucao e a tempera simulada.
"""


import copy
import random
from math import exp
from typing import Dict, List, Tuple
from state import State
from sudoku import Sudoku


class SimulatedAnnealingSudokuSolver:
    def __init__(
        self, initial_sudoku_problem: Sudoku, stale_limit: int = 500
    ):
        self.initial_sudoku_problem = initial_sudoku_problem
        self.fixed_positions_dict = self.__find_fixed_positions()
        self.stale_limit = stale_limit

    def __find_fixed_positions(self) -> Dict[int, List[int]]:
        """ Encontra as celulas fornecidas inicialmente no Sudoku e as armazena em um dicionario em que a chave
        representa a submatriz no tabuleiro e o valor uma lista de numeros entre 0 e 8 indicando a ordem da celula
        :param None
        :return fixed_positions_dict: Dicionario contendo as celulas que nao podem ser alteradas durante a execucao
        do algoritmo
        """

        fixed_positions_dict: Dict[int, List[int]] = dict()
        for board_index in range(9):
            board_fixed_positions: List[int] = []
            for row in range(3):
                for column in range(3):
                    board = self.initial_sudoku_problem.boards[board_index]
                    if board[row, column] != 0:
                        board_fixed_positions.append(3 * row + column)
            fixed_positions_dict[board_index] = board_fixed_positions
        return fixed_positions_dict

    def __generate_first_state(self) -> State:
        """ Gera o estado inicial de entrada do algoritmo a partir da instancial original do problema, preenchendo-se
        as celulas vazias
        :param None
        :return first_state: objeto do tipo State contendo o Sudoku inicial com as celulas vazias preenchidas de valores
        escolhidos aleatoriamentes no intervalo de 1 a 9
        """

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
        """ Rotina principal do algoritmo de tempera simulada. A cada iteracao um novo estado e gerado a partir
        do estado atual com a rotina de perturbacao do estado, a qualidade do novo estado e calculada e se essa for
        maior do qua a qualidade do estado atual, aceitamos o novo estado como atual e atualizamos a energia do sistema,
        caso a qualidade nao seja maior, ainda podemos aceita-lo com a probabilidade de e^(delta/T), em que delta e a
        variacao da qualidade do estado atual e o possivel novo estado e T representa a temperatura atual do sistema.
        A cada iteracao a temperatura e decrescida de um fator ate chegar a 0, momento em que o algoritmo
        obrigatoriamente para e retorna a melhor solucao encontrada ate o momento.
        :param None
        :return current_state, current_score: uma tupla contendo o ultimo estado obtido apos a temperatura do sistema
        chegar a 0 e a pontuacao desse estado, idealmente, essa pontuacao deve valer 1, consequentemente, o estado
        retornado deve conter o Sudoku resolvido
        """

        current_state: State = self.__generate_first_state()
        current_score: float = current_state.get_score()
        initial_temperature = 50000
        temperature = initial_temperature
        stale_points = 0
      
        print("\n\nResolvendo...\n\n")
        while temperature > 0 and current_score != 1:
            possible_best_state: State = State(copy.deepcopy(current_state.sudoku_problem))
            possible_best_state.disturb(self.fixed_positions_dict)
            possible_best_score = possible_best_state.get_score()
            delta_score = possible_best_score - current_score
            accept_new_state: bool = False

            if delta_score > 0:
                accept_new_state = True
                stale_points = 0
            elif exp(delta_score / temperature) > random.random():
                accept_new_state = True
            if accept_new_state:
                current_score = possible_best_score
                current_state = possible_best_state
            else:
                stale_points += 1

            if stale_points > self.stale_limit:
                temperature = initial_temperature
                current_state = self.__generate_first_state()
                current_score = current_state.get_score()
                stale_points = 0

            temperature *= 0.6

        return current_state, current_score
