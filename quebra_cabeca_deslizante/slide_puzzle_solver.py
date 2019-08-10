from __future__ import annotations

import random
import sys
from functools import reduce
from itertools import repeat
from typing import List
import operator
import math
import copy


class StateMatrix:
    def __init__(self, rows: int, columns: int, elements: List[List]):
        self.rows = rows
        self.columns = columns
        self.elements = elements

    def __str__(self):
        msg: str = ""
        hyphens_qt: int = (9 * self.columns - 1)
        msg += "\n+{}+\n".format(hyphens_qt * "-")
        for i in range(self.rows):
            for j in range(self.columns):
                msg += "|  {x:^4}  ".format(x=str(self.elements[i][j])
                                            if self.elements[i][j] != self.rows * self.columns
                                            else " ")  # o bloco vazio é o de maior valor na sequência do puzzle
            msg += "|\n"
            if i != self.rows - 1:
                msg += "|{}|\n".format(hyphens_qt * "-")
        msg += "+{}+\n".format(hyphens_qt * "-")
        return msg

    def is_solved(self) -> bool:
        for i in range(self.rows):
            for j in range(self.columns):
                if self.elements[i][j] != self.rows*i + j + 1:
                    return False
        return True

    def get_element_position(self, element: int) -> tuple:
        cords: List[tuple] = [(ind, self.elements[ind].index(element)) for ind in range(len(self.elements))
                              if element in self.elements[ind]]
        return cords[0]

    def get_blank_space_position(self) -> tuple:
        # o bloco vazio é o valor mais alto na sequência de números do puzzle que varia de acordo com o tamanho deste
        blank_value: int = self.rows * self.columns
        cords: tuple = self.get_element_position(blank_value)
        return cords

    def calculate_manhattan_distance(self, element: int) -> int:
        if element not in [item for sublist in self.elements for item in sublist]:
            return math.inf  # se o elemento não existe na matriz sua distância é infinita

        row_expected: int = (element - 1) // self.columns
        column_expected: int = (element - 1) % self.rows

        element_position: tuple = self.get_element_position(element)

        row_distance: int = abs(row_expected - element_position[0])
        column_distance: int = abs(column_expected - element_position[1])

        manhattan_distance: int = row_distance + column_distance
        return manhattan_distance


class TreeNode:
    def __init__(self, matrix: StateMatrix, tree_layer: int, children: List[TreeNode] = None, parent: TreeNode = None):
        self.matrix = matrix
        if children is None:
            self.children = []
        else:
            self.children = children
        self.parent = parent
        self.tree_layer = tree_layer

    # heurística para estimar quão distante da solução o nó está, quanto menor o valor, melhor
    def get_distance_from_solution(self) -> int:
        distance: int = self.tree_layer

        distance += reduce(operator.add, map(self.matrix.calculate_manhattan_distance,
                                             [item for sublist in self.matrix.elements for item in sublist]))

        return distance

    def generate_possible_states(self):
        permutations: List[dict] = []
        up: dict = {"row": -1, "column": 0}
        left: dict = {"row": 0, "column": -1}
        down: dict = {"row": 1, "column": 0}
        right: dict = {"row": 0, "column": 1}
        permutations.extend([up, down, left, right])

        for permutation in permutations:
            blank_position: tuple = self.matrix.get_blank_space_position()

            blank_row: int = blank_position[0]
            blank_column: int = blank_position[1]

            swap_row: int = permutation["row"] + blank_row
            swap_column: int = permutation["column"] + blank_column
            # o estado possível só será criado se a célula a ser trocada estiver dentro dos limites da matriz
            if 0 <= swap_row < self.matrix.rows and 0 <= swap_column < self.matrix.columns:
                # como a cópia de lista no python é, por padrão, shallow, precisamos fazer uma deep copy, pois
                # vamos alterar a matriz de estados, mas queremos manter a matriz original inalterada
                copy_matrix: List[List] = copy.deepcopy(self.matrix.elements)
                child_state: StateMatrix = StateMatrix(self.matrix.rows, self.matrix.columns, copy_matrix)

                blank_value: int = self.matrix.rows * self.matrix.columns
                swap_value: int = child_state.elements[swap_row][swap_column]

                child_state.elements[swap_row][swap_column] = blank_value
                child_state.elements[blank_row][blank_column] = swap_value

                node_child: TreeNode = TreeNode(child_state, self.tree_layer + 1, parent=self)
                self.children.append(node_child)


class StateTree:
    def __init__(self, root: TreeNode):
        self.root = root

    # método para encontrar o caminho de um nó até a raíz da árvore
    def find_path_to_root(self, node: TreeNode) -> List[TreeNode]:
        path: List[TreeNode] = []
        current_node: TreeNode = node
        while current_node != self.root:
            path.append(current_node)
            current_node = current_node.parent
        path.append(current_node)
        path.reverse()  # a lista está de trás para frente, então precisamos usar o reverse
        return path


class SlidePuzzleSolver:
    def __init__(self, decision_tree: StateTree):
        self.decision_tree: StateTree = decision_tree
        self.puzzle_rows: int = decision_tree.root.matrix.rows
        self.puzzle_columns: int = decision_tree.root.matrix.columns

    def solve(self):
        self.show_header_message()

    def show_header_message(self):
        print("\n\nResolvendo instância do problema quebra cabeça deslizante.\nNúmero de linhas: {}"
              "\nNúmero de colunas: {}\n\nEstado inicial: {}\n\n".format(self.puzzle_rows, self.puzzle_columns,
                                                                         self.decision_tree.root.matrix))


def generate_random_matrix(order: int) -> StateMatrix:
    elements: List = [x + 1 for x in range(order**2)]
    random.shuffle(elements)
    matrix: List[List] = [elements[index:index + order] for index in range(0, len(elements), order)]
    state_matrix: StateMatrix = StateMatrix(order, order, matrix)
    return state_matrix


def main():
    matrix_oder: int = 3
    try:
        arg: int = int(sys.argv[1])
        if arg > 1:
            matrix_oder = arg
            print("\nUtilizando valor argumento {} como ordem da matriz do puzzle.".format(matrix_oder))
        else:
            print("\nUtilizando valor padrão {} como ordem da matriz do puzzle, pois o valor passado como "
                  "argumento ({}) é menor que o mínimo aceitável(2).".format(matrix_oder, int(sys.argv[1])))
    except (ValueError, IndexError):
        print("\nUtilizando valor padrão {} como ordem da matriz do puzzle.".format(matrix_oder))
        pass

    initial_matrix_state: StateMatrix = generate_random_matrix(matrix_oder)
    root: TreeNode = TreeNode(initial_matrix_state, 0)
    tree: StateTree = StateTree(root)

    slide_puzzle_solver: SlidePuzzleSolver = SlidePuzzleSolver(tree)
    slide_puzzle_solver.solve()


if __name__ == '__main__':
    main()
