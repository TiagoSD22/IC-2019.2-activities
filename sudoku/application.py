from datetime import datetime
import random
import time
from numpy import array
from typing import List
from simulated_annealing import SimulatedAnnealingSudokuSolver
from sudoku import Sudoku
from mocks import mock_list
import logging


def make_mock() -> List[array]:  # funcao para gerar um sudoku mockado para testes
    mock = random.choice(mock_list)
    return mock


def run(mock):

    # tabuleiro mockado para testes
    #mock = make_mock()
    #sudoku: Sudoku = Sudoku(mock[1])

    date_time_obj = datetime.now()
    timestamp = date_time_obj.strftime("%d-%b-%Y (%H:%M:%S)")
    file_name: str = "sudoku-" + mock[0] + "-" + timestamp + ".log"

    logger = logging.getLogger("sudoku_solver")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    sudoku: Sudoku = Sudoku(mock)

    sudoku: Sudoku = Sudoku(mock[1], logger)

    print(
        "\n\nCaso: {}\n{}\nPontuacao: {}".format(
            mock[0], sudoku, sudoku.calculate_fitness()
        )
    )
    logger.debug(f"Caso: {mock[0]}\n{sudoku}")

    sa: SimulatedAnnealingSudokuSolver = SimulatedAnnealingSudokuSolver(
        sudoku, logger, 500
    )
    start = time.time()
    final_state, score = sa.solve()
    final = time.time()
    print("Ultimo estado encontrado:\n{}\nPontuacao: {}\nTempo: {}s.".format(final_state, score, (final - start)))

    print(
        "Ultimo estado encontrado:\n{}\nPontuacao: {}\nTempo: {}s.".format(
            final_state, score, (final - start)
        )
    )
    logger.debug(
        f"Ultimo estado encontrado:\n{final_state}\nPontuacao: {score}\nTempo: {(final - start)}s."
    )


if __name__ == "__main__":
    main()
