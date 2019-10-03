import random
import time
from numpy import array
from typing import List
from simulated_annealing import SimulatedAnnealingSudokuSolver
from sudoku import Sudoku
from mocks import mock_list


def make_mock() -> List[array]:  # funcao para gerar um sudoku mockado para testes
    mock = random.choice(mock_list)
    return mock


def run(mock):

    sudoku: Sudoku = Sudoku(mock)

    print("Caso: {}\n{}".format(mock[0], sudoku))
    #print("Fitness: ", sudoku.calculate_fitness())

    sa: SimulatedAnnealingSudokuSolver = SimulatedAnnealingSudokuSolver(sudoku, 500)
    start = time.time()
    final_state, score = sa.solve()
    final = time.time()
    print("Ultimo estado encontrado:\n{}\nPontuacao: {}\nTempo: {}s.".format(final_state, score, (final - start)))
