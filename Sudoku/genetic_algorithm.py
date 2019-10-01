import copy
import operator
import random
from typing import List, Dict, Tuple
from numpy import array
from sudoku import Sudoku


class SudokuGeneticAlgorithm:
    def __init__(self, sudoku: Sudoku, population_size: int):
        self.initial_sudoku: Sudoku = sudoku
        self.population_size: int = population_size

    def generate_individual(self) -> Sudoku:
        values: List[int] = [v for v in range(1, 10)]
        new_individual: Sudoku = copy.deepcopy(self.initial_sudoku)
        for row in range(9):
            for column in range(9):
                sub_board: int = 3 * (row // 3) + (column // 3)
                cell_value: int = self.initial_sudoku.boards[sub_board][
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
                                for row in new_individual.boards[sub_board]
                                for value in row
                            ]
                        ]
                    )
                    new_individual.boards[sub_board][row % 3, column % 3] = new_value

        return new_individual

    def generate_initial_population(self) -> List[Sudoku]:
        population: List[Sudoku] = []
        for n in range(self.population_size):
            individual: Sudoku = self.generate_individual()
            population.append(individual)

        return population

    # retorna uma lista de tuplas (int, float) com o indice do elemento dentro da populacao e o fitness dele
    def rank_population(self, population) -> List[int]:
        fitness_results: Dict[int, float] = {}

        for i in range(self.population_size):
            fitness_results[i] = population[i].calculate_fitness()

        return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)

    @staticmethod
    def tournament_selection(
        population: List[Sudoku], tournament_size: int
    ) -> Tuple[Sudoku, Sudoku]:
        best_individual: Sudoku = None
        # selecionando o primeiro individuo
        for i in range(tournament_size):
            chosen: Sudoku = random.choice(population)
            if (
                best_individual is None
                or chosen.calculate_fitness() > best_individual.calculate_fitness()
            ):
                best_individual = chosen

        second_best_individual: Sudoku = None
        # selecionando o segundo individuo
        population_without_first_individual = [
            ind for ind in population if ind != best_individual
        ]
        for i in range(tournament_size):
            chosen: Sudoku = random.choice(population_without_first_individual)
            if (
                second_best_individual is None
                or chosen.calculate_fitness()
                > second_best_individual.calculate_fitness()
            ):
                second_best_individual = chosen

        return best_individual, second_best_individual

    def breed(self, parent1: Sudoku, parent2: Sudoku) -> Tuple[Sudoku, Sudoku]:
        child1_rows: List = []
        child2_columns: List = []

        for i in range(9):
            row_parent1_score = parent1.get_row_score(i)
            row_parent2_score = parent2.get_row_score(i)
            if row_parent1_score > row_parent2_score:
                best_row = parent1.get_row(i)
            else:
                best_row = parent2.get_row(i)
            child1_rows.append(best_row)

            column_parent1_score = parent1.get_column_score(i)
            column_parent2_score = parent2.get_column_score(i)
            if column_parent1_score > column_parent2_score:
                best_column = parent1.get_column(i)
            else:
                best_column = parent2.get_column(i)
            child2_columns.append(best_column)

        child1_sub_boards: List[array] = []
        child2_sub_boards: List[array] = []
        for i in range(9):
            base_index: int = 3 * (i // 3)  # para acessar o elemento da lista de linhas
            sub_index: int = 3 * (i % 3)  # para acessar os elementos da linha
            row1: List = []
            row2: List = []
            row3: List = []
            col1: List = []
            col2: List = []
            col3: List = []
            for j in range(sub_index, sub_index + 3):
                row1.append(child1_rows[base_index][j])
                row2.append(child1_rows[base_index + 1][j])
                row3.append(child1_rows[base_index + 2][j])

                col1.append(child2_columns[base_index][j])
                col2.append(child2_columns[base_index + 1][j])
                col3.append(child2_columns[base_index + 2][j])

            child1_sub_boards.append(array([row1, row2, row3]))
            child2_sub_boards.append(array([col1, col2, col3]).transpose())

        child1: Sudoku = Sudoku(child1_sub_boards)
        child2: Sudoku = Sudoku(child2_sub_boards)
        return child1, child2


