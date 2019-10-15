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

    sudoku: Sudoku = Sudoku(data)

    sa: SimulatedAnnealingSudokuSolver = SimulatedAnnealingSudokuSolver(sudoku)

    solved, score = sa.solve()

    res = []
    for board in solved.sudoku_problem.boards:
        res.append(board.tolist())
    return jsonify(res)


if __name__ == '__main__':
    app.run(port=5050)
