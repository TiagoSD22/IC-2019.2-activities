import logging
from datetime import datetime

from flask import Flask, request, jsonify, json
from flask_cors import CORS, cross_origin
import numpy

from simulated_annealing import SimulatedAnnealingSudokuSolver
from sudoku import Sudoku

import time

app = Flask(__name__)
CORS(app)


@app.route('/solve', methods=["POST"])
@cross_origin()
def process():
    data = numpy.asarray(request.get_json())

    date_time_obj = datetime.now()
    timestamp = date_time_obj.strftime("%d-%b-%Y (%H:%M:%S)")
    file_name: str = "sudoku-" + "teste" + "-" + timestamp + ".log"

    logger = logging.getLogger("sudoku_solver")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    sudoku: Sudoku = Sudoku(data, logger)

    sa: SimulatedAnnealingSudokuSolver = SimulatedAnnealingSudokuSolver(sudoku, logger)
    start = time.time()
    solved, score = sa.solve()
    final = time.time()

    print("Tempo total: ", final - start)
    res = []
    for board in solved.sudoku_problem.boards:
        res.append(board.tolist())
    return jsonify(res)


if __name__ == '__main__':
    app.run()
