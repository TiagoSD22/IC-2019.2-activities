from numpy import array
from typing import List

from genetic_algorithm import SudokuGeneticAlgorithm
from sudoku import Sudoku


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

    ga = SudokuGeneticAlgorithm(sudoku, 100)
    pop = ga.generate_initial_population()
    for ind in pop:
        print("\n\nIndividuo: \n", ind)
        print("Fitness: ", ind.calculate_fitness())
    #print(ga.rank_population(pop)[0])

    ga.breed(pop[99], pop[98])


if __name__ == "__main__":
    main()